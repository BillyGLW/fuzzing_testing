import subprocess
import sys
import glob
import random
import time

MAX_MUTATED_BYTES = 0.01
BINARY_PATH = "asdf"

def select_file(path):
  file_rand_choice = random.choice(glob.glob(path))
  with open(file_rand_choice, "rb") as f:
    return bytearray(f.read())

def mutate(d):
  if not d:
    return d

  max_n = int(len(d) * MAX_MUTATED_BYTES)
  if max_n == 0:
    max_n = 1

  n = random.randint(1, max_n)

  for _ in range(n):
    idx = random.randint(0, len(d) - 1)
    d[idx] = random.randint(0, 255)

def execute(d):
  with open("sample.bin", "wb") as f:
    f.write(d)
  
  try:
    cp = subprocess.run(
      [
          "gdb", "--batch",  "--return-child-result", "-x", "fuzz.gdb",
          BINARY_PATH
      ],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
      timeout=2.0)
  except subprocess.TimeoutExpired as e:
    sys.stdout.write("T")
    return (False, "")

  report = ""
  magic = "------------------------------"
  # crashed = cp.returncode >= 0xc0000000
  crashed = cp.returncode >= 2
  if crashed:
    report = cp.stdout.split(magic)
  return (crashed, report)
    #print(cp.stdout)



def write_sample(d, report):
  fn = "crashes/%.8i_%.8i" % (int(time.time()), random.randint(0, 123456))
  with open(fn + ".bin", "wb") as f:
    f.write(d)
  with open(fn + ".txt", "wb") as f:
    f.write(bytes(str(report), "utf-8"))
  print("Crash written as: %s" % fn)

def main():

  while True:
    d = select_file("corpus/*")
    mutate(d)
 
    crashed, report = execute(d)
    if crashed:
      write_sample(d, report)

    sys.stdout.write(".")
    sys.stdout.flush()

if __name__ == "__main__":
  main()

