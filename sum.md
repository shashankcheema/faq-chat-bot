# Data Science Batch Models Monitoring Dashboards in Datadog

## Leadership Monitoring Dashboard

### Overview

This section serves as a guide for leadership to understand and effectively utilize the custom-built monitoring dashboard in Datadog, designed specifically for overseeing Data Science Batch Models. The dashboard consists of 8 widgets, each providing crucial insights into the performance and health of the batch processing jobs.

### Widgets Breakdown

#### 1. Number of Jobs
- **Purpose**: Displays the total number of batch processing jobs executed.

#### 2. Success Rate
- **Calculation**: Pods that are successful / Total number of pods

#### 3. Failure Rate
- **Calculation**: Pods that are failed / Total number of pods

#### 4. Number of Pods Failed
- **Purpose**: Shows the count of failed pods.

#### 5. Number of Pods Failed due to OOM
- **Purpose**: Counts pods that failed because of Out-Of-Memory (OOM) issues.

#### 6. Number of Container Restarts
- **Purpose**: Tracks how many times containers within the pods have restarted.

#### 7. Number of Pods Failed due to Crash Loop Back-Off Errors
- **Purpose**: Quantifies failures specifically attributed to crash loop back-off errors.

#### 8. Number of Pending Pods
- **Purpose**: Indicates the count of pods that are in a pending state and haven’t started execution.

## Engineering Monitoring Dashboard

### Overview

This document assists engineering teams in understanding and using the Engineering Monitoring Dashboard in Datadog, tailored for Data Science Batch Models. It is divided into two sections: Overview and Detailed Pod/Container Information.

### Overview Section Widgets

#### 1. Number of Jobs
- **Purpose**: Displays the total count of batch jobs executed.

#### 2. Successful Jobs
- **Purpose**: Shows the count of jobs completed successfully.

#### 3. Failed Jobs
- **Purpose**: Counts the number of jobs that have failed.

#### 4. Number of Pods Failed due to OOM
- **Purpose**: Tracks failures specifically due to Out-of-Memory errors.

#### 5. Number of Container Restarts
- **Purpose**: Indicates how often containers are being restarted.

#### 6. Number of Pods Failed due to Crash Loop Back-Off Errors
- **Purpose**: Quantifies failures from crash loop back-off errors.

#### 7. Pods in Bad Phase (Pending, Failed)
- **Purpose**: Shows pods in non-optimal states.

#### 8. Top Cron Jobs by Job Count
- **Purpose**: Identifies the most frequently run cron jobs.

#### 9. Events Widget from OCP
- **Purpose**: Displays OpenShift Container Platform events.

#### 10. CronJob Resource Consumption
- **Purpose**: Monitors the resource usage of cron jobs.

#### 11-15. Time Series of Resource Usage (CPU, Memory, Disk, Network) and Network Errors by Cron Job

### Detailed Pod/Container Information

#### 1-11. Time Series and State Information for Pods and Containers
- **Purpose**: These widgets provide granular details about pod and container states, resource usage, and errors.

## Utilizing the Dashboards for Incident Resolution

1. **Identify the Issue**: Use the Overview widgets to detect spikes in failed jobs or resource overutilization.
2. **Drill Down**: Employ the Detailed Pod/Container Information to pinpoint affected containers or pods.
3. **Analyze and Resolve**: Examine logs, error messages, and resource metrics for root cause analysis and apply necessary fixes.
4. **Monitor Post-Resolution**: Continuously monitor the dashboard to ensure the issue is resolved and to prevent recurrence.

## Conclusion

These dashboards in Datadog are strategic tools for both leadership and engineering teams to maintain oversight and manage the health and performance of Data Science Batch Models. Regular engagement with these dashboards ensures sustained operational efficiency and effectiveness.
