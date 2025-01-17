import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Customer Trusted
CustomerTrusted_node1701758303907 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="CustomerTrusted_node1701758303907",
)

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1701758303285 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/accelerometer/landing/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerLanding_node1701758303285",
)

# Script generated for node Join
Join_node1701758433577 = Join.apply(
    frame1=AccelerometerLanding_node1701758303285,
    frame2=CustomerTrusted_node1701758303907,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="Join_node1701758433577",
)

# Script generated for node Drop Fields
DropFields_node1701758584291 = DropFields.apply(
    frame=Join_node1701758433577,
    paths=[
        "serialNumber",
        "birthDay",
        "shareWithResearchAsOfDate",
        "shareWithPublicAsOfDate",
        "registrationDate",
        "customerName",
        "shareWithFriendsAsOfDate",
        "email",
        "lastUpdateDate",
        "phone",
    ],
    transformation_ctx="DropFields_node1701758584291",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1701758656517 = glueContext.getSink(
    path="s3://human-balance-analytics-project/accelerometer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="AccelerometerTrusted_node1701758656517",
)
AccelerometerTrusted_node1701758656517.setCatalogInfo(
    catalogDatabase="human-balance-analytics-project",
    catalogTableName="accelerometer_trusted",
)
AccelerometerTrusted_node1701758656517.setFormat("json")
AccelerometerTrusted_node1701758656517.writeFrame(DropFields_node1701758584291)
job.commit()