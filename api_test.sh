#!/bin/bash

echo " >>> Passing meaningless string as an image content:"
image='bla-bla-bla'
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"test_image.jpg","body":"'$image'"}' \
  http://localhost:5000/api/inspect_image


echo
echo " >>> Passing a simple image:"
image=$(base64 -w0 test_images/image.jpg)
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"normalisation":"on", "name":"test_image.jpg","body":"'$image'"}' \
  http://localhost:5000/api/inspect_image

echo
echo " >>> Passing a complex test image:"
image=$(base64 -w0 test_images/557C0F8B32AF5F8B50D4F560FF443B2A.jpg)
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"normalisation":"on", "name":"test_image.jpg", "body":"'$image'"}' \
  http://localhost:5000/api/inspect_image

