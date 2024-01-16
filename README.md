# Intro
In Trigo's solution there are many proprietary sensors based on embedded microcontrollers running bare-metal OS under hard resources limit (low cpu, low memory). Those sensors cannot run any modern tools such as Docker, Consul agents and so on but do expose an http server with a dedicated metrics endpoint.

In addition, the store operators can change the participating sensors so the inventory of sensors can be updated quite often.

In this exercise we are going to implement custom service discovery for prometheus so even when the sensors configuration is changed continously, prometheus will keep monitoring the right sensor's inventory.

# Exercise
The [inventory service](https://github.com/trigovision/devops_exercise/tree/main/prometheus_custom_sd/inventory_server) will be used to expose an http endpoint that yields a list of hosts of the current active sensors.

Specifically, invoking the following command:
```
curl -XGET http://localhost:1337/inventory
```
will yield the current sensors hostnames to monitor:
```
[
    "sensor_1",
    "sensor_2",
    "sensor_12",
    ...
]
```

Your goal in this excersice is to:
* Implement a custom service discovery for prometheus which queries the described endpoint (in the `inventory service`) and yields a target group containing the sensors targets
* Write a minimal docker-compose / helm chart which runs the entire stack, having a prometheus instance trying to scrape the sensors inventory with an exposed http port (tcp/9090)



# Additional Notes
* Don't change the `inventory service` code.
* Fork this repository and upload your solution then provide us with a link.
* Feel free to code it in any language you would like and use any framework / library / snippet of code you find.
* We are avaialbe for any question you have so feel free to ask.

# My Solution:
The files that got added by me:
1) custom_sd.py: queries the inventory service endpoint and generates a Prometheus target group configuration.
2) docker-compose.yml: run Prometheus, the custom service discovery script, and the inventory service.
3) prometheus.yml: includes the custom service discovery configuration.
4) Dockerfile.custom-sd: build the custom service discovery image.

Building and Running the Stack:
1) Build the custom service discovery image:
docker-compose build
2) Run the entire stack:
docker-compose up

Now, Prometheus should be able to discover and scrape the sensors based on the custom service discovery. The configuration includes the custom service discovery job, which queries the /inventory endpoint of the custom service discovery script (custom-sd) to dynamically update the target group.

How to validate it's working:
1) Check Docker Containers:
Use the following command to ensure that all containers are running without issues:
docker-compose ps
This should show all services (inventory-service, custom-sd, prometheus) as "Up."
2) Access Prometheus UI:
Open your web browser and go to http://localhost:9090 (or the appropriate IP address or domain if running remotely). This should open the Prometheus web UI.
3) Validate Targets:
In the Prometheus UI, navigate to the "Targets" tab. It should show the targets that Prometheus is scraping.
4) Query Metrics:
You can use the Prometheus UI to run queries and verify that metrics are being collected. For example, try querying metrics related to your sensors.
5) Check Custom Service Discovery Endpoint:
Open a new terminal and use curl to check the /inventory endpoint of the custom service discovery:
curl http://localhost:5000/inventory
This should return a JSON array containing the current sensors' hostnames.
note: you can check in your browser by running url http://localhost:9090 for prometheus, http://localhost:1337/inventory for inventory-service, http://localhost:5001/inventory for custom-sd service
6) Review Logs:
Check the logs of the containers to see if there are any error messages or unexpected behavior:
docker-compose logs
note: You can use this command to view the logs of specific services, e.g., `docker-compose logs prometheus`.

By performing these steps, you can ensure that the entire stack is working as expected. If any issues arise, review the logs for error messages, and adjust the configurations accordingly.