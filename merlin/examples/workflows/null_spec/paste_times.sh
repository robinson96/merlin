
concurrencies=(1 2 4 8 16 32 64)
samples=(1 10 100 1000 10000)
read_path="/g/g13/bay1/null_results"

touch my_data.yaml

for c in "${concurrencies[@]}"
    do
    for s in "${samples[@]}"
        do
        echo "c${c}_s${s} : " >> my_data.yaml
        python3 task_script.py ${read_path}/c_$c/s_$s/*.log >> my_data.yaml
        done
    done
perl -pi -e 's/ : \n/ : /g' my_data.yaml
