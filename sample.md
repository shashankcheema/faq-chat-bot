
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

## Pros of the Sidecar Approach

- **Modularity**: The sidecar approach allows for a modular design, where additional functionalities can be added without altering the core application. This enhances maintainability and scalability.
- **Isolation**: By isolating additional processing in a sidecar container, the risk of impacting the main application is minimized. This leads to better fault tolerance.
- **Security**: Existing security measures for accessing Datadog API keys can be reused in the sidecar, maintaining a consistent security model across the application.
- **Flexibility**: Sidecar containers can be developed, tested, and deployed independently of the main application, allowing for more flexible and agile development practices.
- **Resource Management**: Resources can be allocated and managed separately for the main and sidecar containers, optimizing the performance and efficiency of the overall system.
- **Enhanced Capabilities**: The sidecar can extend Birddog’s capabilities to handle monitors, alerts, and dashboards for applications that do not have a service listed in Datadog.


## Detailed Plan

### Development Phase
- Design the Flask application structure.
- Implement API endpoints and Datadog client.
- Write unit and integration tests.

### Configuration Phase
- Define environment variables for inter-container communication.
- Update OpenShift pod specifications to include the sidecar container.
- Configure network policies for secure communication.

### Testing Phase
- Conduct unit and integration testing.
- Perform performance testing to ensure minimal resource usage and optimal efficiency.
- Test inter-container communication and error handling mechanisms.

### Deployment Phase
- Deploy the updated pod configuration to OpenShift.
- Monitor the application for any issues.
- Conduct post-deployment testing to ensure seamless operation.

## OCP Configuration Changes

### Pod Specification
Update the pod specification to include the sidecar container. Define resource limits and requests for both the Birddog and sidecar containers.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: birddog-pod
spec:
  containers:
  - name: birddog-container
    image: birddog-image:latest
    env:
    - name: DATADOG_API_KEY
      valueFrom:
        secretKeyRef:
          name: datadog-secret
          key: api_key
  - name: sidecar-container
    image: sidecar-image:latest
    env:
    - name: SIDE_APP_CONFIG
      value: "config_value"
  resources:
    limits:
      memory: "512Mi"
      cpu: "500m"
    requests:
      memory: "256Mi"
      cpu: "250m"
```

### Network Policies
Configure network policies to allow inter-container communication.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-inter-container-communication
spec:
  podSelector:
    matchLabels:
      app: birddog
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: birddog
    ports:
    - protocol: TCP
      port: 5000
```

### Vault Integration
Ensure that both the Birddog and sidecar containers can access the Vault for Datadog API keys.

## API Design

### Sidecar Flask Application API
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

## Cons and Detailed Remediation

| Cons                                         | Detailed Remediation                                                                                                   |
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **Increased Complexity in Pod Management**   | Implement automated deployment scripts to manage pod configurations and updates. Use Kubernetes ConfigMaps and Secrets for managing configuration and sensitive data.                                                              |
| **Potential Performance Overhead**           | Optimize the sidecar container to use minimal resources. Conduct performance testing to identify bottlenecks and improve efficiency. Monitor resource usage and adjust as needed to maintain optimal performance.            |
| **Robust Error Handling and Recovery**       | Implement comprehensive error handling in the sidecar application. Use retry logic for transient errors and alerting mechanisms to notify about persistent issues. Employ logging and monitoring to quickly identify and address issues. |



## Detailed Execution Plan for Birddog and Sidecar Flask Application Integration

This execution plan outlines the step-by-step process for the development, configuration, testing, and deployment of the sidecar Flask application to be integrated with the existing Birddog application in the OpenShift Container Platform (OCP). The plan is broken down into phases with specific tasks, milestones, and deliverables.

## Phases and Tasks

### Phase 1: Design and Planning

| Task ID | Task Description | Deliverable | Story Points |
|---------|------------------|-------------|--------------|
| 1.1     | Define Flask Application Structure | Documented Flask application structure | 3 |
| 1.2     | Define Inter-Container Communication Protocols | Communication protocol document | 2 |
| 1.3     | Define Environment Variables and Configurations | Environment variable and configuration documentation | 2 |

### Phase 2: Development

| Task ID | Task Description | Deliverable | Story Points |
|---------|------------------|-------------|--------------|
| 2.1     | Implement Flask Application | Flask application codebase | 8 |
| 2.2     | Implement API Endpoints and Datadog Client | Working API endpoints with Datadog integration | 5 |
| 2.3     | Write Unit and Integration Tests | Test scripts and test cases | 3 |

### Phase 3: Configuration

| Task ID | Task Description | Deliverable | Story Points |
|---------|------------------|-------------|--------------|
| 3.1     | Update OpenShift Pod Specifications | Updated YAML pod specification | 2 |
| 3.2     | Configure Network Policies | Network policy configurations | 3 |
| 3.3     | Configure Vault Integration | Vault integration configuration | 2 |

### Phase 4: Testing

| Task ID | Task Description | Deliverable | Story Points |
|---------|------------------|-------------|--------------|
| 4.1     | Conduct Unit and Integration Testing | Test results and bug reports | 5 |
| 4.2     | Perform Performance Testing | Performance test results and optimization recommendations | 3 |
| 4.3     | Test Inter-Container Communication and Error Handling | Test results and bug reports | 4 |

### Phase 5: Deployment

| Task ID | Task Description | Deliverable | Story Points |
|---------|------------------|-------------|--------------|
| 5.1     | Deploy to OpenShift | Deployed application in OpenShift | 3 |
| 5.2     | Monitor Application | Monitoring reports and issue logs | 2 |
| 5.3     | Conduct Post-Deployment Testing | Post-deployment test results | 3 |


## Technical Flow Diagrams

### Communication Flow
1. Request initiated from Birddog container.
2. Birddog sends request to sidecar container.
3. Sidecar processes the request using Datadog API keys from Vault.
4. Sidecar sends response back to Birddog.

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

