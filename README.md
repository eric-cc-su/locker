Locker
===
**Author: [eric-cc-su](https://github.com/eric-cc-su)**

Locker is an ***experimental***, trying-to-learn-new-things, terminal Python password manager. The program uses the `cryptography` Python library to encrypt and store key, password pairs. The idea is to be able to securely save and serve passwords for the user, as well as encrypt the user's files as requested.

#Using Locker

In the terminal, navigate to the Locker directory and run locker.py as a python script

	cd */locker
	python locker.py

###Requirements

- Python 3
- The [Cryptography](https://cryptography.io/en/latest/) Python library

##Initial Authentication

When running Locker, you will first need to supply a "locker combination". Currently (06/24/15), any unrecognized locker combinations will ask the user if they wish to create a new repository. This allows users to have multiple, isolated "databases". Make sure you are using the correct locker combination to access the desired sensitive data.

###List

The `list` function will display the key values in the catalog. This shows the user what key, value pairs they have saved in the database.

Functional

###Import

The `import` function will read a file (preferably .txt) and import key, value pairs into the database from the file data. You need to provide two things to the `import` function:

1. **The filepath**: you will be prompted for the filepath. You may use an absolute or a relative file path. Press Enter to input the formatting.
2. **The formatting**: it is expected that your file is set up in a simple key, value style format. Use `LABEL` to represent the key, and `PWD` to represent the value. `LABEL` and `PWD` are case sensitive and your input should reflect the exact spacing and content of your file's lines.
	- ex: if the lines of your file are set up as: `Facebook - password1`, you will input `LABEL - PWD`.
	- ex: if the lines of your file are more like `password add some words facebook, there was the key` then you will need to input `PWD add some words LABEL, there was the key`

Functional

###New

The `new` function will allow the user to add a new key, value pair. 

In development

###Delete

Delete a key, value pair. 

In development

###Encrypt

`encrypt` will be used to encrypt files unrelated to Locker. The user will provide the filepath and a key to encrypt the file. The file will only be decryptable with the proper key.

In development.


###Decrypt

`decrypt` will be used to serve a key, value pair's value to the user. The user will input the key and the key's value will be decrypted and served to the user. If `encrypt` is developed to encrypt individual files, decrypt will have the ability to either decrypt or serve the file.

In development.

#***DISCLAIMER***

*I know extremely little about developing programs for encryption and security. The `experimental, trying-to-learn-new-things` designation above is* ***EXTREMELY IMPORTANT*** *to note as this is an* ***IN PROGRESS*** *project to teach myself more about Python and security. I am* ***NOT*** *responsible for any lost or compromised sensitive data that may result from the use of this code.*

![You Know Nothing](http://i3.kym-cdn.com/photos/images/newsfeed/000/527/985/04f.gif)

*([Know Your Meme](http://knowyourmeme.com/memes/you-know-nothing-jon-snow))*

*This code is licensed under the MIT License and under copyright by Eric Su*

&copy; 2015 Eric Su
