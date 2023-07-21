# Performance testing PostgreSQL indexes

## DB preparing:

Build PostgreSQL image:

    docker build . -t test-postgres

Run locally:  
    
    docker run -d --cpus=0.5 -m=2g -p 5432:5432 --name test-postgres test-postgres

## Uploading data:
    tbd

## Index tests:

### Hash
    tbd

### B-tree
    tbd

### Bitmap
    tbd

## Cleaning out container and image:

    docker stop test-postgres && docker rmi test-postgres