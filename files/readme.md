# This folder lists the files required for the chatbot to work.
### 1. config.txt
   The file contains the data necessary to launch the chatbot:
   * A list of files containing information about a database of products, stores, car counters, and contacts.
   * Identifiers of admins who can modify data in the bot in "real time".
   * Email addresses for sending and collecting letters of complaints and suggestions using smtp-module.
   * Data required for authorization in the account that collects complaints and suggestions from users: server, login and password of the account that receives messages.
   * TimeOut - the waiting time before work stops and goes into sleep mode. 
### 2. avto.xlsx
   The file contains data on parking places of a truck stop (mobile store), in the format - locality and opening hours.
### 3. price.xlsx
   The file contains a list of products to create a catalog of products for each store in the network. Each item has a name, price in different store categories and unit of measurement for correct display in the catalog.
### 4. contacts.xlsx
   The file contains the names of employees and their contact numbers.
### 5. shops.xlsx
   The file contains store addresses, contact phone numbers, opening hours, store price category and individual identification number.
### 6. chicken.xlsx
   The file contains chicken breeds, delivery cities and phone numbers of contact persons.
