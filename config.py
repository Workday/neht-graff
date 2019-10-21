# Constant configuration values
import os

# Flask Configuration
FLASK_PORT = 8080

# Neo4j Configuration
NEO4J_URI = os.environ['NEO4J_URI']


NEO4J_CREDS = (os.environ['NEO4J_USER'], os.environ['NEO4J_PASSWORD'])
