# Exploring Airflow: Essential and Optional Components

🍭 When exploring Airflow for the first time, you'll likely use the Docker Compose file provided in the Airflow official quick start guide. It works well, but you might wonder about all those services listed in the YAML file. Are they all necessary for a simple deployment? Today, let's examine the components required for a basic Airflow installation on a single machine, as well as some optional components that can help achieve a more scalable Airflow setup.

## Required Components:

- 📌 **A Scheduler:** In the basic setup, the scheduler processes DAG files, triggers scheduled workflows, and submits tasks to the executor to run. Note that the executor is a configuration property of the scheduler, not a separate component. For a simple setup, set “AIRFLOW__CORE__EXECUTOR: LocalExecutor” in your Docker Compose file. 
- 📌 **A Folder to Hold the DAGs:** If it doesn't already exist, the “airflow-init” service in the official Docker Compose file will create the necessary directories. 
- 📌 **A Webserver:** This provides a UI that allows you to monitor the behavior and status of your Airflow DAGs. You can also trigger runs and view logs through the UI.
- 📌 **A Metadata Database:** Airflow components use this database to store state of workflows and tasks.

## To Scale and Run Airflow in a Distributed Environment, Some Optional Components Might Be Needed:

- 📌 **Optional Worker:** This is a separate component that’s not part of the scheduler. It can be run as a long-running process in the CeleryExecutor, or as a pod in the KubernetesExecutor.
- 📌 **Optional Triggerer:** This component executes deferred tasks in an asyncio event loop. Without a standalone triggerer, task deferral is not possible. 
- 📌 **Optional DAG Processor:** If present, it takes over the functionality of parsing DAG files from the scheduler. 
- 📌 **Optional Folder of Plugins:** This extends Airflow’s functionality by allowing for custom operators, hooks, and more.

The advantages of having these components separated also include more flexibility in setting layers of user permission and ensuring better security.

## Learn More

If you're interested in learning more, the ["Architecture Overview" page](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html) of the Airflow official documentation is a great starting point. 

