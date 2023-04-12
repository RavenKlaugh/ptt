docker build -t ptt .
docker run -p 5000:5000 -e OPENAI_API_KEY=youropenaiapikey -e AWS_ACCESS_KEY_ID=youracceskey -e AWS_SECRET_ACCESS_KEY=yoursecretacceskey ptt