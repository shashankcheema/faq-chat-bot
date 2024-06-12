
# Design Document for Birddog and Sidecar Flask Application Integration

## Overview
This document outlines the design and optimization of a new Flask application to be integrated as a sidecar container alongside the existing Birddog application running in OpenShift Container Platform (OCP). The goal is to extend Birddog’s capabilities to handle monitors, alerts, and dashboards for applications that do not have a service listed in Datadog, using JSON or other request formats.

## Current State
Birddog is a Flask application running within a pod on OCP, providing automation for Datadog by allowing users to get, create, and update monitors, alerts, and dashboards. It relies on a specific YAML format and requires the application service to exist in Datadog, LeanIX, and ServiceNow. Datadog API keys are accessed through a Vault init container.

## Proposed Solution
Develop a new Flask application to run as a sidecar container alongside the Birddog application. This sidecar will utilize the Datadog API keys from the main Birddog container and handle requests for applications that are not listed in Datadog.

## Requirements
- **Communication:** Ensure seamless communication between the main Birddog container and the sidecar container.
- **Requests:** Requests will originate from the main Birddog container to the sidecar container.
- **OCP Configurations:** Configure OCP to ensure the Birddog container remains unaffected by the sidecar.
- **Changes to Main Container:** Document all necessary changes to the main Birddog container to support this integration.
- **Cons Remediation:** Address all potential disadvantages of the sidecar approach.

{tabulated_pros_cons}

## Cons Remediation
- **Increased Complexity in Pod Management**: Implement automated deployment scripts to manage pod configurations and updates. Use Kubernetes ConfigMaps and Secrets for managing configuration and sensitive data.
- **Potential Performance Overhead**: Optimize the sidecar container to use minimal resources. Conduct performance testing to identify bottlenecks and improve efficiency.
- **Robust Error Handling and Recovery**: Implement comprehensive error handling in the sidecar application. Use retry logic for transient errors and alerting mechanisms to notify about persistent issues.

## Detailed Plan

1. **Development Phase**:
   - Design the Flask application structure.
   - Implement API endpoints and Datadog client.
   - Write unit and integration tests.

2. **Configuration Phase**:
   - Define environment variables for inter-container communication.
   - Update OpenShift pod specifications to include the sidecar container.
   - Configure network policies for secure communication.

3. **Testing Phase**:
   - Conduct unit and integration testing.
   - Perform performance testing to ensure minimal resource usage and optimal efficiency.
   - Test inter-container communication and error handling mechanisms.

4. **Deployment Phase**:
   - Deploy the updated pod configuration to OpenShift.
   - Monitor the application for any issues.
   - Conduct post-deployment testing to ensure seamless operation.

{ocp_configuration_changes}

## API Design

### Sidecar Flask Application API:
- **Endpoint:** /create_monitor
  - **Method:** POST
  - **Description:** Create a new Datadog monitor.
  - **Request Body:** JSON
  - **Response:** JSON

- **Endpoint:** /update_monitor
  - **Method:** PUT
  - **Description:** Update an existing Datadog monitor.
  - **Request Body:** JSON
  - **Response:** JSON

- **Endpoint:** /get_monitors
  - **Method:** GET
  - **Description:** Retrieve monitors.
  - **Response:** JSON

- **Endpoint:** /create_alert
  - **Method:** POST
  - **Description:** Create a new Datadog alert.
  - **Request Body:** JSON
  - **Response:** JSON

- **Endpoint:** /update_alert
  - **Method:** PUT
  - **Description:** Update an existing Datadog alert.
  - **Request Body:** JSON
  - **Response:** JSON

## Additional Technical Details

### Flask Application Structure
The new Flask application will follow a standard structure:

- **app/**: Directory containing the Flask application code.
  - **routes.py**: Defines the API endpoints and request handling.
  - **datadog_client.py**: Manages interactions with the Datadog API.
  - **utils.py**: Contains utility functions for request validation and error handling.
  - **config.py**: Configuration settings for the application, including environment variables.
- **tests/**: Directory for unit and integration tests.
  - **test_routes.py**: Tests for API endpoints.
  - **test_datadog_client.py**: Tests for Datadog client interactions.
  - **test_utils.py**: Tests for utility functions.
- **requirements.txt**: Lists the dependencies required for the Flask application.

### Inter-Container Communication
Inter-container communication will be facilitated through the following methods:

- **HTTP Requests**: The main Birddog container will communicate with the sidecar container using HTTP requests. Flask's built-in request handling will be used for this purpose.
- **Environment Variables**: Necessary environment variables for inter-container communication will be defined in the pod specification.

### Security Considerations
- **API Key Management**: The sidecar container will access Datadog API keys from the Vault init container, similar to the main Birddog container.
- **Secure Communication**: HTTPS will be used for communication between the containers to ensure data security.

### Technical Flow Diagram

```plaintext
                                      +------------------+
                                      |                  |
                                      |   DataDog API    |
                                      |                  |
                                      +---------^--------+
                                                |
                                                |
 +---------------------+                +-------+--------+
 |                     |                |                |
 | Vault Init Container|                |  Sidecar Flask |
 |                     +---------------->  Application   |
 |  (Fetch API Keys)   |                |                |
 +----------^----------+                +-------^--------+
            |                                   |
            |                                   |
            |                                   |
            |                           +-------+--------+
 +----------+----------+                |                |
 |                     |                |   Birddog      |
 |   OpenShift Pod     +<---------------+   Application  |
 |                     |(Inter-container|                |
 | - Birddog           | Communication) |                |
 | - Sidecar Flask     |                +----------------+
 | - Vault Init        |
 +---------------------+


### Communication Flow:
1. Request initiated from Birddog container.
2. Birddog sends request to sidecar container.
3. Sidecar processes the request using Datadog API keys from Vault.
4. Sidecar sends response back to Birddog.
