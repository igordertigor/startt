This file illustrates the basic use of startt in a series of cram tests.


## Create a local template folder

We first create a template directory locally. In real life, you would not need
to do this and you only need one template directory in your home directory.

  $ mkdir templates
  $ echo "This is the default template for txt files" > templates/default.txt
  $ echo "This is a specific template for txt files accessible as memo.txt" > templates/memo.txt

The two commands that start with 'cat' simply write non-sense into the
respective files. In real life, you would probably want more meaningful
content. For completeness, we also create a 'folder' template that contains
more than one file.

  $ mkdir templates/multi.html
  $ echo "this is the main html file" > templates/multi.html/main.html
  $ echo "this is an additional style file that just gets linked" > templates/multi.html/style.css

So in total, we now have the following setup

  $ ls templates
  default.txt
  memo.txt
  multi.html

## Showing available templates

If we don't give a filename to startt, it should show all the possible
templates we could have:

  $ startt -t templates
  default.txt
  memo.txt
  multi.html

So, we have three templates. One default template for txt files and then two
specialized templates one for memos in txt format and one called multi.html.

## Using the standard template

First, we want to use the standard txt-file template. To do so, we call

  $ startt -t templates elaborate_name.txt

startt parses the target filename and fills in the content of the default
template for the matching extension. In our case, this creates a file called
'elaborate_name.txt' in the current folder and fills it with the content of the
'default.txt' template. We can check this, by looking at that files content:

  $ cat elaborate_name.txt
  This is the default template for txt files


## Using a specialized template

So far so good. There may be file names for which we would like to have more than one template.
For example, we might want one template just for regular files and one for special "memo" files.
Our current template folder actually supports that.

Let's use the 'memo.txt' template:

  $ startt -t templates name_of_memo_file.memo.txt

To check, we can again look at the content:

  $ cat name_of_memo_file.txt
  This is a specific template for txt files accessible as memo.txt


## Using a multi-file template

For some templates, we might want to use multiple files. For example, we may
have latex letter for which we want to use our institution's logo, or we might
want to include a css file with a html file. To bundle multiple files into one
template, we can use a folder template. For example, when we created our
template folder above, we created a folder called 'multi.html'. Note that the
folder has an extension as well! This is needed for startt's extension matching
to work. In the multi.html folder, we have a couple of files where *one file
has to start with 'main'*. startt will consider this 'main' file as the file
that we actually want to edit, while all other files are considered auxiliary
files. This is important because our main file will be copied to the filename
we specify, while all auxiliary files will just be made available as symbolic
links!

So to tell startt to use our multi.html template, we just run

  $ startt -t templates my_website.multi.html

And startt will copy all the contents of the template into the local folder. We
can check the file contents in our usual way:

  $ cat my_website.html
  this is the main html file

and

  $ cat style.css
  this is an additional style file that just gets linked
