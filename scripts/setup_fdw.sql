-- Script for setting up the Soundcloud FDW
--------------------------------------------

create extension multicorn;

create server scloud_fdw foreign data wrapper multicorn options (
    wrapper 'soundcloud_fdw.SoundcloudFDW.SoundcloudForeignDataWrapper',
    apikey '<your api key here>');

CREATE FOREIGN TABLE scloud (
    title character varying,
    url character varying,
    search character varying
) server scloud_fdw;
