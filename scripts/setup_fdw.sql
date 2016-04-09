-- Script for setting up the Soundcloud FDW
--------------------------------------------

CREATE EXTENSION multicorn;

CREATE SERVER scloud_fdw FOREIGN DATA WRAPPER multicorn OPTIONS (
    wrapper 'soundcloud_fdw.SoundcloudFDW.SoundcloudForeignDataWrapper',
    apikey '<your api key here>');

CREATE FOREIGN TABLE scloud (
    title CHARACTER VARYING,
    url CHARACTER VARYING,
    search CHARACTER VARYING
) SERVER scloud_fdw;
