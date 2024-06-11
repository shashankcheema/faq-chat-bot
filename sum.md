Design Document for Sidecar Flask Application for Birddog
Overview
This document outlines the design for a new Flask application to be deployed as a sidecar container alongside the existing Birddog application. The purpose of this sidecar application is to manage monitors, alerts, and dashboards for applications that do not have a service listed in DataDog and interact via JSON or other request formats. The sidecar will leverage the DataDog API keys from the main Birddog container using a shared Vault init container.

Architecture
The architecture consists of the following components:

Birddog Application: Existing Flask application running in a pod on OCP (OpenShift Container Platform). It handles automation for DataDog.
Sidecar Flask Application: New Flask application running as a sidecar container to manage DataDog entities for services not listed in DataDog.
Vault Init Container: Shared container responsible for fetching and providing DataDog API keys to both the Birddog and sidecar applications.
DataDog API: External service API used for creating, updating, and retrieving monitors, alerts, and dashboards.
LeanIX and ServiceNow: External systems where the services must be registered before interacting with DataDog.
Components Interaction
Vault Init Container: On pod startup, fetches DataDog API keys and makes them available to both the Birddog and sidecar containers.
Birddog Application: Uses the API keys to perform its existing functions.
Sidecar Flask Application: Utilizes the API keys to interact with the DataDog API for services not listed in DataDog.
DataDog API: Receives requests from both the Birddog and sidecar applications.
LeanIX and ServiceNow: Ensure services are registered before any interaction with DataDog.
Detailed Design
Vault Init Container
Function: Initialize and fetch DataDog API keys.
Flow:
Start with the pod.
Fetch DataDog API keys from Vault.
Make the keys available as environment variables or shared files to both Birddog and sidecar containers.
Birddog Application
Existing Functionality: Continue with its current role in managing DataDog monitors, alerts, and dashboards.
Environment: Access API keys from the Vault init container.
Sidecar Flask Application
Purpose: Handle requests for creating, updating, and retrieving DataDog entities for unlisted services.

Endpoints:

POST /monitor: Create a new monitor.
PUT /monitor/<id>: Update an existing monitor.
GET /monitor/<id>: Retrieve a monitor.
POST /alert: Create a new alert.
PUT /alert/<id>: Update an existing alert.
GET /alert/<id>: Retrieve an alert.
POST /dashboard: Create a new dashboard.
PUT /dashboard/<id>: Update an existing dashboard.
GET /dashboard/<id>: Retrieve a dashboard.
Flow:

Receive requests in JSON or other formats.
Utilize the DataDog API keys from the Vault init container.
Interact with the DataDog API to perform the requested operations.
Return appropriate responses.
Environment Setup
Configuration:

Ensure both Birddog and sidecar containers have access to the API keys from the Vault init container.
Set up necessary environment variables for both applications.
Deployment:

Deploy the Birddog application with the sidecar container in the same pod.
Configure the Vault init container to run before the main containers to ensure keys are available.
Security Considerations
Vault Integration: Securely fetch and store API keys using Vault.
Environment Isolation: Ensure the sidecar container cannot interfere with the Birddog container's environment or operations.
Access Control: Restrict access to the sidecar endpoints to authorized users or services only.
Conclusion
By deploying the new Flask application as a sidecar container, we can extend the functionality of the Birddog application to manage DataDog entities for unlisted services. This design ensures efficient use of shared resources, maintains security, and leverages existing infrastructure.

Future Enhancements
Logging and Monitoring: Implement logging and monitoring for the sidecar application to track its performance and usage.
Scaling: Consider scaling the sidecar container independently if needed based on load.
API Gateway: Introduce an API gateway to manage and route requests between the Birddog and sidecar applications efficiently.
