globalvnc
=========

School research project - in-browser VNC client.

Goals
-----

This project aims to be an in-browser VNC client that is
easy to set up on the back end, but configurable enough
that it is versatile.

Origin
------

The need for this became apparent to my team during a
Hackathon; [our project](http://github.com/jholtom/webvirt)
required a VNC client for connecting to VMs, but no
in-browser software we found truly fit our needs.

Requirements
------------

Serverside:
* [tornado](http://github.com/facebook/tornado)

Clientside:
* A web browser that supports Canvas and Websockets
