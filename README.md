# Splitco
This project was created to make my life a little easier as the sole owner of a Costco membership amongst my household of three twenty-something dudes. We would routinely make house trips to Costco and buy $300+ worth of items of which I would have to foot the bill for. Rather than make excel spread sheets with different individuals (myself + roommate 1 + roommate 2, myself + roommate 1, myself + roommate 2) and manually figuring out how to divide the item costs appropriately I figured a flexible document structure such as JSON and Python functions would expedite the process significantly. This process could extend to other situations quite easily as well since it doesn't really care how many contributors there are or who they are. The only real dependency at the moment is Pandas which is rather frequently installed in base environments if you don't want to deal with the pipenv virtual environment.

The first step is to create a JSON document with the following structure:
```json
{
    "description": "store-name",
    "timestamp": "01/01/2021",
    "items": [
    {
        "item": "item1",
        "cost": 15.49,
        "adjustment": -0.20,
        "contributors":["Person1","Person2","Person3"]
    },
    {
        "item": "item2",
        "cost": 11.52,
        "adjustment": 0.00,
        "contributors":["Person1","Person2"]
    },
    {
        "item": "item3",
        "cost": 49.99,
        "adjustment": 0.00,
        "contributors":["Person2","Person3"]
    }]
}
```

We'll refer to this JSON document as `receipt-template.json` throughout the rest of this README. The next step is to throw this file in the `input` directory. From there the process is relatively simple. Just call the `splitco.py` script with your input file as the only argument similar to the following (it automatically looks in the input directory):
```bash
python3 splitco.py receipt-template.json
```

Ultimately, the command will print a pandas dataframe with each person's associated costs for a given item as well as their total costs. Additionally a file with the format `{description}-{date}.csv` will be output to the output directory if you need to refer to it at a later time or send to someone else. 

```bash
$ python3 splitco.py receipt-template.json
         Person1    Person2    Person3
item                                  
item1   5.096667   5.096667   5.096667
item2   5.760000   5.760000   0.000000
item3   0.000000  24.995000  24.995000
total  10.856667  35.851667  30.091667
```
