argv = sys.argv[1:]
print("argv:", argv)
# Task for MB: Please fix sbatch argv command line
result=subprocess.run("sbatch argv".split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print ("Result: ",result)
used_wallclock = False
used_exclusive = False
with open('test.sub') as f:
    for l in f.readlines():
        if not l.startswith('#SBATCH'):
            continue
        if ('--exclusive' in l):
            used_exclusive = True
        if ('-t' in l):
            used_wallclock = True
            #To-do: If user doesn't request for all the cores on the node on full.q, do not let them submit the job
        if ('full.q' in l):
                print("You are submitting your job to full.q without requesting for full node. Please use this flag IF and ONLY IF you are using all the cores on the node")
                         
jid = result.stdout.decode().split(' ')[-1].strip()

if used_exclusive:
    with open('exclusive_jobs', 'a') as f:
        f.write('Job' +str(jid) +'was submitted with exclusive')
    print("WARNING: You are using --exclusive flag in your submission file. This blocks other users from running jobs on the same node as your job. Please use this flag IF and ONLY IF you are absolutely sure you need an entire node")
if used_wallclock == False:
    print ("You have not specified a wall-clock limit for your job to run. Please specify wall-clock time for scheduler to schedule your jobs more efficiently")