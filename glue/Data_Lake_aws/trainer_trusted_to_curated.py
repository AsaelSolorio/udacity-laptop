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

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1701934122997 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/accelerometer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerTrusted_node1701934122997",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1701934125660 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://human-balance-analytics-project/step_trainer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerTrusted_node1701934125660",
)

# Script generated for node JOIN
SqlQuery0 = """
select distinct sensorreadingtime, distancefromobject, x, y, z, user, serialnumber 
from act 
join stt on stt.sensorreadingtime = act.timestamp
"""
JOIN_node1701934196942 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={
        "act": AccelerometerTrusted_node1701934122997,
        "stt": StepTrainerTrusted_node1701934125660,
    },
    transformation_ctx="JOIN_node1701934196942",
)

# Script generated for node machine learning curated
machinelearningcurated_node1701934639056 = glueContext.getSink(
    path="s3://human-balance-analytics-project/machine-learning/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="machinelearningcurated_node1701934639056",
)
machinelearningcurated_node1701934639056.setCatalogInfo(
    catalogDatabase="human-balance-analytics-project",
    catalogTableName="machine_learning_curated",
)
machinelearningcurated_node1701934639056.setFormat("json")
machinelearningcurated_node1701934639056.writeFrame(JOIN_node1701934196942)
job.commit()