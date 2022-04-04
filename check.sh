#!/bin/bash

echo "Passing meaningless string as an image content."
image='bla-bla-bla'
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"test_image.jpg","body":"'$image'"}' \
  http://localhost:5000/api/check_image


echo
echo "Passing image without searched objects."
image=$(base64 -w40960 test_images/image.jpg)
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"test_image.jpg","body":"'$image'"}' \
  http://localhost:5000/api/check_image

echo
echo "Passing a proper test image."
image=$(base64 -w40960 test_images/557C0F8B32AF5F8B50D4F560FF443B2A.jpg)
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"test_image.jpg","body":"'$image'"}' \
  http://localhost:5000/api/check_image

