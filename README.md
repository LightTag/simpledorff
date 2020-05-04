# SimpleDorff - Calculate Krippendorff's Alpha on a DataFrame

Krippendorff's Alpha is a commonly used inter-annotator reliability metric, but it's hard to calculate on a Dataframe. This package makes it easy.

Made with ❤️ by [LightTag - The Text Annotation Tool For Teams](https://lighttag.io). We use this in production to give our customers a single number to understand the quality of their labeled data. Read the [blog post here](https://lighttag.io/blog/krippendorffs-alpha/)  

## Problem It Solves

Calculating Krippendorff's Alpha assumes data is formatted in a way that just doesn't appear in the wild. We wanted a package that could read a Dataframe in the formats we see in real life and give us the Alpha in one line. 

## Installing
```bash
pip install simpledorff
```

## Usage


```python

```


```python
import simpledorff
import pandas as pd
Data = pd.read_csv('./examples/from_paper.csv') #Load Your Dataframe
Data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>document_id</th>
      <th>annotator_id</th>
      <th>annotation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>A</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>B</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>1</td>
      <td>D</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>1</td>
      <td>C</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>2</td>
      <td>A</td>
      <td>2.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
simpledorff.calculate_krippendorffs_alpha_for_df(Data,experiment_col='document_id',
                                                 annotator_col='annotator_id',
                                                 class_col='annotation')
```




    0.743421052631579


