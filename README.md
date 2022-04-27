# cv_flow_examples

Fill in the appropriate fields in .cnvrg_auth

## To Run locally on your laptop
Run `export $(cat .cnvrg_auth | xargs)` to apply them into your environment variables

install the sdk `pip3 install cnvrgv2`

## To run from within a docker container (sdk already installed)
docker run -it --rm --env-file=.cnvrg_auth -v $(pwd):/root/test nctiggy/cnvrgv2 /bin/ash

files will be in `cd /root/test`
