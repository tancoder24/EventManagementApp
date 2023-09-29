# Commit History
![WhatsApp Image 2023-09-29 at 16 46 10](https://github.com/tancoder24/EventManagementApp/assets/78148494/b451c363-d617-40b9-ba0b-e27933937d8b)
![WhatsApp Image 2023-09-29 at 16 46 43](https://github.com/tancoder24/EventManagementApp/assets/78148494/3c700a93-cf2b-411d-9ac4-6ac299e6b270)
![WhatsApp Image 2023-09-29 at 16 47 02](https://github.com/tancoder24/EventManagementApp/assets/78148494/c3345d48-92dc-4c15-a4e2-15b0e0620156)


# EventManagementApp


## Prerequisites

Before you begin, ensure you have met the following requirements:

* Docker installed on your system.
* `docker-compose` installed on your system.

## Installation

To get started with the project, follow these steps:

### Clone the Repository:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 gizmo:dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span> </span><button class="flex ml-auto gizmo:ml-0 gap-2 items-center"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="icon-sm" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg> </button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language- ">git clone https://github.com/tancoder24/EventManagementApp
cd EventManagementApp
</code></div></div></pre>

### Install Docker and Docker-Compose:

* Follow the official Docker documentation to install Docker and `docker-compose` on your system.

### Build the Docker Containers:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 gizmo:dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span> </span><button class="flex ml-auto gizmo:ml-0 gap-2 items-center"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="icon-sm" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg> </button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language- ">sudo make build
</code></div></div></pre>

### Apply Database Migrations:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 gizmo:dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span> </span><button class="flex ml-auto gizmo:ml-0 gap-2 items-center"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="icon-sm" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg> </button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language- ">sudo make migrate
</code></div></div></pre>

### Create a Superuser:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 gizmo:dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span> </span><button class="flex ml-auto gizmo:ml-0 gap-2 items-center"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="icon-sm" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg> </button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language- ">sudo make createsuperuser
</code></div></div></pre>

### Start the Application:

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 gizmo:dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span> </span><button class="flex ml-auto gizmo:ml-0 gap-2 items-center"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="icon-sm" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg> </button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language- ">sudo make start
</code></div></div></pre>

### Access the Admin Panel:

* Open your web browser and navigate to: [http://0.0.0.0:8000/api/admin](http://0.0.0.0:8000/api/admin)
* Log in using the superuser credentials you created.

## API Documentation

For API endpoints and requests, refer to the Postman collection included in this repository.
