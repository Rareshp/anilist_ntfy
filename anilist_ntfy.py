import json
import requests
import time
import os
import configparser

basepath   = os.environ['HOME']
configFile = os.path.join(basepath, '.config/anilist_ntfy.conf')
config = configparser.RawConfigParser()
config.read(configFile)

secrets = dict(config.items('Secrets'))
token   = secrets['token']

settings = dict(config.items('Settings'))
ntfyAddress = settings['ntfyaddress']
ntfyTopic   = settings['ntfytopic']
minuteInterval = settings['minuteinterval']
magicTime   = int(minuteInterval) * 60
currentTime = int(time.time())

# Define the GraphQL query
# see: https://studio.apollographql.com/sandbox/explorer for https://graphql.anilist.co
query = '''
query {
    page: Page {
        notifications: notifications {
            ... on AiringNotification {
                id
                type
                animeId
                episode
                contexts
                createdAt
                media: media {
                    id
                    title { userPreferred }
                    type
                    bannerImage
                    siteUrl
                }
            }
            ... on RelatedMediaAdditionNotification {
                id
                type
                mediaId
                context
                createdAt
                media: media {
                    id
                    title { userPreferred }
                    type
                    bannerImage
                    siteUrl
                }
            }
        }
    }
}
'''

# Set up the headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

# Make the request
response = requests.post(
    'https://graphql.anilist.co',
    json={'query': query},
    headers=headers
)

data = response.json()

# Check for errors in the response
if 'errors' in data:
    print("Errors:", data['errors'])
else:
    # Extract notifications
    notifications = data['data']['page']['notifications']

    for notification in notifications:
        if 'createdAt' in notification:
            # Check if the notification is new enough (in seconds)
            if currentTime - notification['createdAt'] < magicTime:
                if 'episode' in notification and 'media' in notification:
                    # print(notification['id'])
                    title = notification['media']['title']['userPreferred']
                    banner = ""
                    if 'bannerImage' in notification['media']:
                        banner = notification['media']['bannerImage']

                    ntfy_body = f"Episode {notification['episode']} of '{title}'"
                    requests.post(f"{ntfyAddress}/{ntfyTopic}",
                        data=ntfy_body,
                        headers={
                            "Title": "New episode aired",
                            "Tags": "dash",
                             # "X-Delay": "10m",
                            "Attach": banner
                        })
    else:
        print("No new notifications found.")

