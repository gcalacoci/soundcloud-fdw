# soundcloud-multicorn-postgresql-fdw
## Multicorn based PostgreSQL Foreign Data Wrapper for Soundcloud

This is a simple FDW that performs searches to Soundcloud using
the [soundcloud python library](https://github.com/soundcloud/soundcloud-python)
as client.

## How To Use The FDW:

* You need a Soundcloud api key, register a new app here: http://soundcloud.com/you/apps 
* Next you'll need Multicorn installed on your PostgreSQL.
*  You'll need to download THIS repository
  * `git clone ssh://git@git.2ndquadrant.it/2ndquadrant-it/gcalacoci/soundcloud-fdw.git
*  You also need to install the python *soundcloud* library:
  * `pip install soundcloud`
* Add your apikey to the config.py file
*  And install its code into your database server as well:
  * `python ./setup.py install`
* Create the multicorn extension:
  * `create extension multicorn;`
* Create a **server** and a **foreign table**.
  * `CREATE SERVER m_soundcloud foreign data wrapper multicorn options (wrapper 'soundcloud_fdw.SoundcloudFDW.SoundcloudForeignDataWrapper');`
  * `CREATE FOREIGN TABLE scloud (title character varying, url character varying, search character varying) server m_soundcloud;`
* Perform searches using the `search` field of the foreign table
  * `select * from scloud where search = 'queen';`

enjoy the results ;)
