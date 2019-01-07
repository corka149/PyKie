```
 _  ___         __              _                                     
| |/ (_) ___   / _| ___  _ __  | |__  _   _ _ __ ___   __ _ _ __  ___ 
| ' /| |/ _ \ | |_ / _ \| '__| | '_ \| | | | '_ ` _ \ / _` | '_ \/ __|
| . \| |  __/ |  _| (_) | |    | | | | |_| | | | | | | (_| | | | \__ \
|_|\_\_|\___| |_|  \___/|_|    |_| |_|\__,_|_| |_| |_|\__,_|_| |_|___/
```


# pykie

At the initial start of this project pykie should be just a collection of useful scripts
to manage Redhat's [Kie-Server](http://jbpm.org/) and take away the pain from controlling it.
The transformation in a real library started after noticing the usefulness.

## Tests

Run all tests with
```bash
python -m unittest discover test
```

## Useful scripts

1. <b>Container undeployer</b>: Undeploys gracefully a kie-container through stopping all related process instances.
2. <b>Show process variables</b>: Shows process variables with a short keystroke