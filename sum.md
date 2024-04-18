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

#### Deployment on OpenShift

*   **Containerization**: Each component of the system is containerized, ensuring scalability and isolation.
*   **Security Measures**: Implement HTTPS for all interactions, utilize OpenShift’s security features for network policies, and secure sensitive data management.
*   **Load Balancing and Auto-Scaling**: Leverage OpenShift features to manage load effectively and scale components based on demand.
