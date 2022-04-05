FLASK-YOLO5
===========

This simple Python script creates a REST/UI WEB application that can detect objects in images.<br><br>

## INSTALLATION

I used conda environment, you may do the same with pyenv, poetry, or whatever pleases you the most.
```
conda create -n pytorch python=3.8
conda activate pytorch
conda install pytorch flask torchvision torchaudio cudatoolkit=11.3 -c pytorch
pip3 install yolo5 python-dotenv 

-- OR --

pip3 install -r requirements.txt
```
<br>

## USAGE

1. Start the application with the `flask run` command.
2. Open address http://127.0.0.1:5000 in the WEB browser.
3. Optionally, send an REST API call to http://127.0.0.1:5000/api/inspect_image.

**NOTE:** The API request should look like this:
```
{
    "name": "image_file_name.jpg",
    "body": "<BASE64 encoded image>"
}
```

Check `api_test.sh` script for more examples.<br><br>

## AUTHOR
Dmitrii Ageev <dmitrii@opsworks.ru>
