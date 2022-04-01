#Run duckhunt levels
import re
import subprocess
import argparse
import sys

def run_level(level, duration):
    #Run level and get output of run
    #Run shell command python3 duck_hunt_main.py -d $duration -l $x
    output = subprocess.check_output(["python3", "duck_hunt_main.py", "-d", str(duration), "-l", str(level)])
    
    #Parse output of run
    #Get #{'hits': ?.?, 'total_ducks': ?, 'scores': {?: ?.?}} using regex

    #Find dictionary in output
    dict = re.findall(r"\{\'hits\': (\d+\.\d+), \'total_ducks\': (\d+), \'scores\': \{(.*): (\d+\.\d+)\}", output.decode("utf-8"))
    hits = dict[0][0]
    total_ducks = dict[0][1]
    score = dict[0][2]
    ratio = dict[0][3]

    return {'hits': hits, 'total_ducks': total_ducks, 'score': score, 'ratio': ratio}

def main(levels, duration):

    #Open file to write results
    f = open("results.csv", "a")

    #Write header
    f.write("level, duration, hits, total_ducks, score, ratio\n")
    f.close()
    
    for level in range(levels[0], levels[1]+1):
        f = open("results.csv", "a")
        #print("Running level", level)
        score = run_level(level, duration)
        #print(score)
        f.write(
            str(level) + ", " + 
            str(duration) + ", " + 
            str(score['hits']) + ", " + 
            str(score['total_ducks']) + ", " + 
            str(score['score']) + ", " + 
            str(score['ratio']) 
            + "\n")
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run duckhunt levels')
    parser.add_argument('-l', '--levels', nargs=2, type=int, help='Range of levels to run')
    parser.add_argument('-d', '--duration', type=int, help='Duration of each level')
    args = parser.parse_args()
    levels = (args.levels[0], args.levels[1])
    duration = args.duration
    main(levels, duration)
