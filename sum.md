#### Authentication Flow Using the Login Endpoint

1.  **User Request**: The user or client application makes a GET request to `/login`.
2.  **Redirect to Okta**: The API responds with a redirection to the Okta login page, passing along the necessary OAuth 2.0 parameters such as `client_id`, `response_type`, `scope`, and `redirect_uri`.
3.  **User Logs In at Okta**: The user enters their credentials on the Okta login page, which securely handles the authentication.
4.  **Authorization Code**: Upon successful authentication, Okta redirects back to the specified `redirect_uri` with an authorization code.
5.  **Exchange Code for Token**: The client application then makes a request to the Okta token endpoint to exchange the authorization code for an access token and, optionally, a refresh token.
6.  **Access Secured Endpoints**: With the access token, the user can now make requests to the secured endpoints of our REST API.

#### Security and Authentication

*   **OAuth 2.0 with Okta**:
    *   Okta serves as the authorization server, providing robust user authentication and token management.
    *   Implements RBAC within Okta to manage roles and access permissions effectively.
    *   All API interactions require valid OAuth 2.0 tokens to ensure that requests are authenticated and authorized according to the user's roles.

#### Database Design

*   **Tables**:
    *   **Logs Table**: Records details about API requests and user activities.
    *   **Sessions Table**: Manages session details and active user tokens.
    *   **Optional Cache Table**: Improves performance by caching frequent data requests, reducing direct calls to Datadog.
### High-Level Database Design

#### 1\. Logs Table

This table records details about API requests and user activities for auditing and monitoring purposes.

**SQL DDL**:

sqlCopy code

`CREATE TABLE logs (     log_id SERIAL PRIMARY KEY,     user_id INTEGER NOT NULL,     endpoint VARCHAR(255) NOT NULL,     action VARCHAR(50) NOT NULL,     response_status INTEGER NOT NULL,     timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,     details TEXT );`

*   **log\_id**: Unique identifier for the log entry.
*   **user\_id**: Identifier of the user who made the request.
*   **endpoint**: API endpoint that was accessed.
*   **action**: Type of action performed (e.g., GET, POST, PUT, DELETE).
*   **response\_status**: HTTP status code returned.
*   **timestamp**: Time when the request was made.
*   **details**: Additional details about the request or action.

#### 2\. Sessions Table

Manages session details and active user tokens. This is crucial for handling user sessions securely.

**SQL DDL**:

sqlCopy code

`CREATE TABLE sessions (     session_id VARCHAR(255) PRIMARY KEY,     user_id INTEGER NOT NULL,     valid_from TIMESTAMP NOT NULL,     valid_until TIMESTAMP NOT NULL,     token TEXT NOT NULL );`

*   **session\_id**: Unique identifier for the session.
*   **user\_id**: Identifier of the user to whom the session belongs.
*   **valid\_from**: Start time of the session.
*   **valid\_until**: Expiry time of the session.
*   **token**: The OAuth token associated with the session.

#### 3\. Users Table

Stores information about users, which is useful for linking log entries and sessions to specific users, as well as managing user-specific data.

**SQL DDL**:

sqlCopy code

`CREATE TABLE users (     user_id SERIAL PRIMARY KEY,     username VARCHAR(255) UNIQUE NOT NULL,     password_hash VARCHAR(255) NOT NULL,     role VARCHAR(50) NOT NULL );`

*   **user\_id**: Unique identifier for the user.
*   **username**: Username of the user.
*   **password\_hash**: Hash of the user’s password (if local authentication mechanisms are used).
*   **role**: The role of the user as defined in RBAC.

#### 4\. Cache Table (Optional)

Improves performance by caching frequent data requests, reducing direct calls to Datadog.

**SQL DDL**:

sqlCopy code

`CREATE TABLE cache (     cache_id SERIAL PRIMARY KEY,     endpoint VARCHAR(255) NOT NULL,     response_data TEXT NOT NULL,     last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP );`

*   **cache\_id**: Unique identifier for the cache entry.
*   **endpoint**: API endpoint for which data is cached.
*   **response\_data**: Cached data for the endpoint.
*   **last\_updated**: Last time the cache was updated.

#### Deployment on OpenShift

*   **Containerization**: Each component of the system is containerized, ensuring scalability and isolation.
*   **Security Measures**: Implement HTTPS for all interactions, utilize OpenShift’s security features for network policies, and secure sensitive data management.
*   **Load Balancing and Auto-Scaling**: Leverage OpenShift features to manage load effectively and scale components based on demand.
