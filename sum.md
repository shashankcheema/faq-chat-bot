+----------------+        +----------------+        +------------------+
|                |        |                |        |                  |
| Client         |        | REST API       |        | Datadog SDK      |
| Applications   +------->+ Layer          +------->+ (Direct API      |
| (Web, Mobile,  |        | (Java/Spring   |        |  Integration)    |
| CLI)           |        | Boot)          |        |                  |
|                |<------>+                |<------>+                  |
+-----+----------+        |                |        +---------+--------+
      |                   |                |                  |
      |                   |                |                  |
      |                   +-------+--------+                  |
      |                           |                           |
      |                           |                           |
      |                           |                           |
      |                   +-------v--------+                  |
      |                   |                |                  |
      |                   | Okta           |                  |
      |                   | Authorization  |                  |
      |                   | Server         |                  |
      |                   |                |                  |
      |                   +-------+--------+                  |
      |                           |                           |
      |                           |                           |
+-----v----------+      +--------v---------+        +---------v--------+
|                |      |                  |        |                  |
| Database       |<-----+ REST API         |<------>+ Datadog SDK      |
| (User, Session,|      | Layer (Handles   |        | (Handles data    |
|  Logs, Cache)  |      | Data Management) |        |  caching)        |
|                |      |                  |        |                  |
+----------------+      +------------------+        +------------------+

