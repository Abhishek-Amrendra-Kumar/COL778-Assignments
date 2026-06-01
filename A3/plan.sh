# Generate a plan and save it to a 
#python downward/fast-downward.py --alias seq-sat-lama-2011 ./pddl_files/$1/domain.pddl ./pddl_files/$1/problem.pddl #> temp.txt
python downward/fast-downward.py --search-time-limit $2 \
  --alias seq-sat-fdss-2023 \
  ./pddl_files/$1/domain.pddl \
  ./pddl_files/$1/problem.pddl 
rm -rf tmp.txt
#it will generate sas_plan.$n file 

# Find the file with the largest number
max_file=$(ls sas_plan.* 2>/dev/null | sort -t. -k2 -n | tail -n 1)

# If no files exist, exit
[ -z "$max_file" ] && { echo "No sas_plan.* files found"; exit 1; }

# Delete all other sas_plan.* files
for f in sas_plan.*; do
    if [ "$f" != "$max_file" ]; then
        rm "$f"
    fi
done

# Rename the largest one
mv "$max_file"  ./pddl_files/$1/plan.pddl

echo "------THE PLAN IS------"
cat ./pddl_files/$1/plan.pddl
echo "The plan is stored in the file ./pddl_files/$1/plan.pddl"
