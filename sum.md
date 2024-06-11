# Design Document for Sidecar Flask Application for Birddog

## Overview

This document outlines the design for implementing a sidecar Flask application to be deployed alongside the existing Birddog application. The sidecar application will handle DataDog operations for applications that do not have a service listed in DataDog and interact via JSON or other request formats.

## Requirements

1. **Communication**: The main Birddog container and the sidecar Flask application must communicate with each other.
2. **Request Flow**: Requests should originate from the Birddog container and be sent to the sidecar container.
3. **Changes to Main Container**: Necessary modifications to the Birddog container to support the new functionality.

## Architecture

The architecture consists of the following components:
1. **Birddog Application**: Existing Flask application running in a pod on OCP (OpenShift Container Platform). It handles automation for DataDog.
2. **Sidecar Flask Application**: New Flask application running as a sidecar container to manage DataDog entities for services not listed in DataDog.
3. **Vault Init Container**: Shared container responsible for fetching and providing DataDog API keys to both the Birddog and sidecar applications.
4. **DataDog API**: External service API used for creating, updating, and retrieving monitors, alerts, and dashboards.
5. **LeanIX and ServiceNow**: External systems where the services must be registered before interacting with DataDog.

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
