05 · Harborline Ground Services: which transfer bags get a runner

ISM6930 final project. The data are synthetic; the organization and its people are fictional.

WHAT IS IN THIS FOLDER

  brief.md                 Read it first, and more than once: the business, its people, the decision your
                           model informs, and what each column means and when it is known. It is a text file
                           (Markdown): open it in any text editor, or in Colab's file viewer.
  train.csv                Rows with the outcome, to learn from.
  test.csv                 Rows with the outcome, from the same period, to score your chosen model once,
                           at the end.
  holdout_features.csv     Rows from a later period, without the outcome: the rows you submit decisions for.
  submission.json          The format your predictions file must take.
  validate_submission.py   Checks your predictions file's format before you upload it.

The files are as the business exported them: nobody has cleaned them.

LOADING THE DATA IN COLAB

  Upload the CSV files in Colab's Files pane (the folder icon on the left), then:

      import pandas as pd
      train = pd.read_csv("train.csv")

CHECKING YOUR SUBMISSION

  Upload validate_submission.py, submission.json and holdout_features.csv beside your predictions file, then run:

      !python validate_submission.py TeamName_holdout_predictions.csv

The project guide, in the Final project module in Canvas, says what to submit and how it is marked.
