#Run duckhunt levels
import re
import subprocess

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

def main():
    levels = (1, 200)
    duration = 60

    #Open file to write results
    f = open("results.csv", "w")

    #Write header
    f.write("level, duration, hits, total_ducks, score, ratio\n")
    for level in range(levels[0], levels[1]+1):
        print("Running level", level)
        score = run_level(level, duration)
        print(score)
        f.write(
            str(level) + ", " + 
            str(duration) + ", " + 
            str(score['hits']) + ", " + 
            str(score['total_ducks']) + ", " + 
            str(score['score']) + ", " + 
            str(score['ratio']) 
            + "\n")


        


if __name__ == '__main__':
    main()