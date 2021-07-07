# Merlin Docker on a Cisco DevNet Sandbox Nexus 9000

For the main Merlin project and what Merlin does please visit:

[Merlin - Network Magic](https://github.com/automateyournetwork/merlin)

You can now run Merlin against a Nexus 9000 in the Cisco DevNet Sandbox.  We have included a custom script and pre-configured testbed file for this purpose.

>To get started, sign up for a Cisco DevNet account at: [DevNet Sandbox](https://devnetsandbox.cisco.com/RM/Topology)

>Once you are signed in, search for "Nexus" in the search dialog at the top left of the screen.

![DevNet Search](images/03_devnetsb-01.png)

>Select one of the reserved instances - We recommend using the instance running the latest version of NXOS.

![DevNet Reserve](images/03_devnetsb-02.png)

>Click "Reserve" after reviewing the reservation details.

![DevNet Reserve](images/03_devnetsb-03.png)

You will receive an email from Cisco confirming the reservation along with links to download the Cisco AnyConnect VPN Client and instructions for its installation.

**Cisco AnyConnect VPN Client:**

[AnyConnect VPN Client](https://developer.cisco.com/site/sandbox/anyconnect/)

**Installation guide for Cisco AnyConnect VPN Client:**

[AnyConnect PDF](https://devnetsandbox.cisco.com/Docs/VPN_Access/AnyConnect_Installation_Guide.pdf)

>Click the "VPN Access" tab in the DevNet console and review the information in it.

![DevNet VPN Access](images/01_devnetsb-04.png)

**Note:** If this is your first time using the Cisco DevNet Sandbox, make sure to review the information in each of the tabs.

In about 15 to 20 minutes, you should receive another email from Cisco with the VPN credentials for your sandbox, including:

* VPN address and port for the connection
* VPN username
* VPN password

>Connect to the DevNet Sandbox VPN using the Cisco AnyConnect VPN Client

![AnyConnect](images/01_devnetsb-05.png)

Once connected, you will have direct network access to the Nexus 9000 in DevNet.

The "NXOS on Nexus 9k" tab in the DevNet console will show you the details you need to connect to the device, however we have already added this information to the `testbed/testbed_DevNet_Nexus9k_Sandbox.yaml` file.

You can confirm it to be sure.

![AnyConnect](images/03_devnetsb-06.png)

You're now ready to run Merlin against the DevNet Nexus 9000!

* To transform at least 16 common commands run the following pyATS job as a Docker Container:

# WSL2, Ubuntu, and Docker Desktop

1. Follow these instructions 

[Docker Desktop using WSL2](https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2)

![Docker Desktop using WSL2](images/docker_wsl.PNG)

[Docker with WSL2 Backend](https://docs.docker.com/docker-for-windows/wsl/)

![Docker Desktop using WSL2](images/docker_wsl_backend.PNG)

2. After you have WSL2, Ubuntu, and Docker Desktop installed you can proceed with cloning the repository 

``` console

git clone https://github.com/automateyournetwork/merlin_docker_nexus.git

```

3. Use docker-compose to create and build your Docker container and images 

``` console

docker-compose up

```
![Docker-Compose Up](images/creating.PNG)

Now check Docker Desktop - Images to confirm all of your microservices are In Use 

![Docker Images](images/images.PNG)

Next check your Container / Apps and expand merlin_docker_nexus - you should see all of your images and their ports runing 

![Container App](images/container_app.PNG)

Now launch your browser and visit http://localhost:8080 to visit the Nexus 9000 Services Homepage

![Docker Homepage](images/docker_homepage.PNG)

Click any of the links - here is the Show Version micro-service

![Show Version Microservice](images/show_version_microservice.PNG)

Explore the JSON - which is the pyATS parse("show version") output 

![pyATS JSON](images/version_json.PNG)

The YAML 

![YAML](images/version_yaml.PNG)

The Markdown

![Markdown](images/version_md.PNG)

You can also download the CSV version

![CSV](images/ver_csv.PNG)

You can also use the URL as a REST API 

In Postman do an HTTP GET against http://localhost:8080

![Postman Homepage](images/postman01.PNG)

Every microservice has it's own APIs - try http://localhost:8100 for Show Version

![Postman Per Service](images/postman02.PNG)

You can use the HTML Links in the bottom of the body to follow them in Postman 

![Postman Links](images/postman03.PNG)

You can follow these links for the JSON in Postman

![Postman JSON](images/postman04.PNG)

Or the YAML 

![Postman YAML](images/postman05.PNG)

[Back to the main project](https://github.com/automateyournetwork/merlin)