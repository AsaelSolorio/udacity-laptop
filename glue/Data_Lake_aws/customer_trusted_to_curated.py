import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1701761172541 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/accelerometer/landing/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerLanding_node1701761172541",
)

# Script generated for node Customer Trusted
CustomerTrusted_node1701761170902 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="CustomerTrusted_node1701761170902",
)

# Script generated for node Join
Join_node1701761263358 = Join.apply(
    frame1=AccelerometerLanding_node1701761172541,
    frame2=CustomerTrusted_node1701761170902,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="Join_node1701761263358",
)

# Script generated for node Drop Fields
DropFields_node1701762111984 = DropFields.apply(
    frame=Join_node1701761263358,
    paths=["z", "y", "x", "user"],
    transformation_ctx="DropFields_node1701762111984",
)

# Script generated for node Drop Duplicates
DropDuplicates_node1701762872309 = DynamicFrame.fromDF(
    DropFields_node1701762111984.toDF().dropDuplicates(["email"]),
    glueContext,
    "DropDuplicates_node1701762872309",
)

# Script generated for node Customer Curated
CustomerCurated_node1701762510604 = glueContext.getSink(
    path="s3://human-balance-analytics-project/customer/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="CustomerCurated_node1701762510604",
)
CustomerCurated_node1701762510604.setCatalogInfo(
    catalogDatabase="human-balance-analytics-project",
    catalogTableName="customer_curated",
)
CustomerCurated_node1701762510604.setFormat("json")
CustomerCurated_node1701762510604.writeFrame(DropDuplicates_node1701762872309)
job.commit()