# Fuzz testing

### Purpose
make able to test input in the most "automatic way as possible"

### set-up

```
set disassembly-flavor intel
echo ------------------------------
r sample.bin
where
i r
x/10i $eip
echo ------------------------------
```
setting intel flavor, running sample.bin (mutated asdf file), print out some disassembly info for later debugging.

### gdb params

```
    "gdb", "--batch",  "--return-child-result", "-x", "fuzz.gdb"
```
means,
batch mode - exit after proccess quit, return child result - being able to print out the results and trace it over again
(crash result is being written in '/crashes' directory), -x specyfies users commands, r sample.bin; using sample.bin as argv[1]
(equivalent ./asdf sample.bin).
