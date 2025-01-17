import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Step Trainer Landing
StepTrainerLanding_node1701843905865 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerLanding_node1701843905865",
)

# Script generated for node Customer Curated
CustomerCurated_node1701843906494 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/customer/curated/"],
        "recurse": True,
    },
    transformation_ctx="CustomerCurated_node1701843906494",
)

# Script generated for node SQL Query
SqlQuery0 = """
select sensorreadingtime, st.serialnumber as serialnumber, distancefromobject 
from st 
join cc 
on st.serialnumber = cc.serialnumber;
"""
SQLQuery_node1701843984767 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={
        "st": StepTrainerLanding_node1701843905865,
        "cc": CustomerCurated_node1701843906494,
    },
    transformation_ctx="SQLQuery_node1701843984767",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1701844155179 = glueContext.getSink(
    path="s3://human-balance-analytics-project/step_trainer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="StepTrainerTrusted_node1701844155179",
)
StepTrainerTrusted_node1701844155179.setCatalogInfo(
    catalogDatabase="human-balance-analytics-project",
    catalogTableName="step_trainer_trusted",
)
StepTrainerTrusted_node1701844155179.setFormat("json")
StepTrainerTrusted_node1701844155179.writeFrame(SQLQuery_node1701843984767)
job.commit()