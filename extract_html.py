#!/usr/bin/env python

import io
from glob import glob
from bs4 import BeautifulSoup

def main():
    names = [x.strip().split(",")
             for x in io.open("data/names", encoding="utf-8")]
    countries = {}

    for n in names:
        role = n[2].strip()
        if role not in ["Team", "Leaders"]:
            continue

        country = n[0].strip()
        if country not in countries:
            countries[country] = {}

        year = int(n[1].strip())
        if year not in countries[country]:
            countries[country][year] = []

        name = n[3].strip()
        img = n[4].strip()
        countries[country][year].append((role, name, img))


    for country in sorted(countries.keys()):
        years = countries[country]
        with io.open("html/%s.html" % country, "w", encoding="utf-8") as f:
            f.write(PRE)

            for year in sorted(years.keys()):
                names = years[year]
                index = 0
                for role, name, img in sorted(names):
                    f.write(ROW % {
                        "role": role,
                        "year": year,
                        "name": name,
                        "img": IMG % img if img != '' else '',
                        "index": str(index),
                    })
                    index += 1
            f.write(POST % country)






PRE = u"""\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Questionnaire on the female presence at the IOI">
    <meta name="author" content="Stefano Maggiolo">

    <title>Female presence at the IOI: questionnaire</title>

    <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">
    <script src="https://code.jquery.com/jquery-1.11.2.min.js"></script>
    <script src="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>

    <style>
      body {
        margin: 20px auto;
        max-width: 600px;
      }
      h1 {
        font-weight: bold;
        margin: 50px 0 15px;
        font-size:28px;
      }
      .program {
        border: 1px solid black;
        margin: 10px;
        padding: 10px;
        background-color: #e7e7e7;
      }
      label {
        display: block;
        font-weight: normal;
        font-style: italic;
      }
      table {
        width: 100%;
      }
      table img {
        height: 90px;
        padding: 2px 5px;
      }
      table input {
        padding: 0 10px;
      }
      table tr {
        height: 100px;
      }
      table tr.selected td {
        background-color: #f7f7f7;
      }
      td {
        padding: 5px 0 5px 10px;
        border: 1px solid black;
        background-color: #e7e7e7;
      }
    </style>

    <script>

var current = 0;

var keybindings = function(ev) {
  var focus = $(document.activeElement);
  if (focus.hasClass('ignorekey')) {
    return;
  }
  var elements = $($('tr')[current]).children('td').children('input');

  if (ev.keyCode == 109) {
    $(elements[0]).prop('checked', true);
    current += 1;
    selectCurrent(true);
  } else if (ev.keyCode == 102) {
    $(elements[1]).prop('checked', true);
    current += 1;
    selectCurrent(true);
  } else if (ev.keyCode == 111) {
    $(elements[2]).prop('checked', true);
    current += 1;
    selectCurrent(true);
  } else if (ev.keyCode == 98) {
    if (current > 0) {
      current -= 1;
    }
    selectCurrent(true);
  }
};

var selectCurrent = function(scroll) {
  $('tr').removeClass('selected');
  var tr = $($('tr')[current]);
  tr.addClass('selected');
  if (scroll == true) {
    $('html, body').animate({
      scrollTop: tr.offset().top
    }, 100);
  }
}

$(document).keypress(keybindings);
$(document).ready(selectCurrent);
$(document).ready(function() {
  $('#email').focus();
});

var removeProgram = function(el) {
  if (confirm("Are you sure you want to remove this program?")) {
    $(el).parent().remove();
  }
};

var addProgram = function(el) {
  $(el).before(
    '<div class="program">' +
    '  <label>' +
    '    <div>Start year of this program</div>' +
    '    <input class="program-start ignorekey" type="text" size="20"></input>' +
    '  </label>' +

    '  <label>' +
    '    <div>End year of this program (leave empty if still running)</div>' +
    '    <input class="program-end ignorekey" type="text" size="20"></input>' +
    '  </label>' +

    '  <label>' +
    '    <div>Description of the program</div>' +
    '    <textarea class="program-desc ignorekey" rows="4" cols="60"></textarea>' +
    '  </label>' +

    '  <label>' +
    '    <div>Outcome of the program</div>' +
    '    <textarea class="program-outcome ignorekey" rows="4" cols="60"></textarea>' +
    '  </label>' +

    '  <label>' +
    '    <div>Reason for discontinuation, if applicable</div>' +
    '    <textarea class="program-reason ignorekey" rows="4" cols="60"></textarea>' +
    '  </label>' +

    '  <button onclick="removeProgram(this)">Remove this program</button>' +
    '</div>');
};

var generate = function() {
  var output = {};
  output['email'] = $('#email').val();
  output['otherinfo'] = $('#otherinfo').val();

  output['programs'] = [];
  var programs = $('.program');
  for (var i = 0; i < programs.length; i++) {
    var program = $(programs[i]);
    var outProgram = {};
    outProgram['start'] = program.find('.program-start').val();
    outProgram['end'] = program.find('.program-end').val();
    outProgram['desc'] = program.find('.program-desc').val();
    outProgram['outcome'] = program.find('.program-outcome').val();
    outProgram['reason'] = program.find('.program-reason').val();
    output['programs'].push(outProgram);
  }

  output['first-total'] = $('#first-total').val();
  output['first-perc'] = $('#first-perc').val();
  output['nationals-total'] = $('#nationals-total').val();
  output['nationals-perc'] = $('#nationals-perc').val();
  output['training-total'] = $('#training-total').val();
  output['training-perc'] = $('#training-perc').val();

  output['people'] = [];
  var trs = $('tr');
  for (var i = 0; i < trs.length; i++) {
    var tr = $(trs[i]);
    var outPerson = {};
    var name = tr.find('input:radio:checked').attr('name');
    if (name) {
      outPerson['name'] = name;
      outPerson['gender'] = tr.find('input:radio:checked').val();
      output['people'].push(outPerson);
    }
  }
  $('#output').val(JSON.stringify(output));
  $('#output').select();
};

$(document).ready(function() { addProgram($('#add-program')); });

    </script>
  </head>

  <body>

    <!--
    <strong style="color: red">
      Someone already completed the questionnaire for this
      country. Feel free to complete the first section again to give a
      different perspective, but there is no need to fill the genders
      of the team members.
    </strong>
    -->

    <h1>About you</h1>
    <label>
      <div>An e-mail address in case I need to ask more questions</div>
      <input id="email" class="ignorekey" type="email" size="60"></input>
    </label>

    <h1>About your country's team selection</h1>

    <p>I am interested in knowing if the Olympic Committee for your
    country has or had some program or rules acting on the female
    presence at the Olympiad (both on a national and international
    level.</p>

    <p>Some examples of such programs or rules:</p>
    <ul>
      <li>a minimum/maximum number of female participants in the team
        at IOI;</li>
      <li>a minimum/maximum number of female participants at some
        specific stage of the selection process;</li>
      <li>programs to encourage female students to apply for the IOI
        selections;</li>
      <li>programs to expose female students to the IOIs, or to
        computer science;</li>
      <li>mentorship or training programs focused on female
        students.</li>
    </ul>

    <p>For each of these programs, please add a section specifying the
    years in which the program was in place, a brief description, and
    the outcomes. If the program was discontinued, please add the
    reason.</p>

    <button id="add-program" onclick="addProgram(this)">Add another program</button>

    <br/>
    <hr/>
    <br/>

    <p>The following are some questions about the number of students
    taking part in your country's IOI selections. Please answer with
    the average of the last three years.</p>

    <p>The questions are about total number of participants and female
    percentage at three stages of the selection:</p>
    <ul>
      <li>at the very beginning: the first competition, usually
      distributed in the schools throughout the country;</li>
      <li>at the "national IOI" stage: usually an onsite (but possibly
      online) contest with tens or low hundreds of participants, that
      might or might not assign a title;</li>
      <li>at the training stage: when students receive (usually
      onsite, but also online) dedicated training, usually from
      previous contestants, or experts in the field.</li>
    </ul>

    <p>Feel free to leave blank an answer if you cannot provide a good
    estimate.</p>

    <strong>First selection</strong>

    <label>
      <div>How many students in total take part?</div>
      <input id="first-total" class="ignorekey" type="text" size="60"></input>
    </label>

    <label>
      <div>What is the percentage of female participants (0-100)?</div>
      <input id="first-perc" class="ignorekey" type="text" size="60"></input>
    </label>

    <strong>National IOI</strong>

    <label>
      <div>How many students in total take part?</div>
      <input id="nationals-total" class="ignorekey" type="text" size="60"></input>
    </label>

    <label>
      <div>What is the percentage of female participants (0-100)?</div>
      <input id="nationals-perc" class="ignorekey" type="text" size="60"></input>
    </label>

    <strong>Training</strong>

    <label>
      <div>How many students in total take part?</div>
      <input id="training-total" class="ignorekey" type="text" size="60"></input>
    </label>

    <label>
      <div>What is the percentage of female participants (0-100)?</div>
      <input id="training-perc" class="ignorekey" type="text" size="60"></input>
    </label>

    <br/>
    <hr/>
    <br/>

    <label>
      <div>Any other relevant information?</div>
      <textarea id="otherinfo" rows="4" cols="60"></textarea>
    </label>

    <h1>About your country's teams</h1>

    <p>In each row of the following table there is a member of a
    delegation of your country. Please select the gender for each of
    them. To make this process faster, you can use these keys to
    select a value for the highlighted person (after selecting the
    first with your mouse):</p>
    <ul>
      <li><strong>m</strong> for male;
      <li><strong>f</strong> for female;
      <li><strong>o</strong> for other / not sure;
      <li><strong>b</strong> to go back to the previous person.
    </ul>

    <table>
"""


POST = u"""\
    </table>

    <h1>Send the information</h1>

    <p>Last step! Please click on "Generate" and send me an email at
    <a href="mailto:s.maggiolo@gmail.com?subject=Questionnaire for %s" target="_blank">
      s.maggiolo@gmail.com
    </a>
    copying and pasting or attaching the content of the following
    area. The output will be pre-selected, so Ctrl-C/cmd-C is enough
    to copy everything.</p>

    <button onclick="generate()">Generate</button><br/>
    <textarea id="output" class="ignorekey" rows="10" cols="60"></textarea>

  </body>
</html>
"""


ROW = u"""\
      <tr>
        <td>%(year)s</td>
        <td>%(role)s</td>
        <td>%(img)s</td>
        <td>%(name)s</td>
        <td>
          <input type="radio" name="%(year)s-%(role)s-%(index)s" value="m">Male</input></br>
          <input type="radio" name="%(year)s-%(role)s-%(index)s" value="f">Female</input></br>
          <input type="radio" name="%(year)s-%(role)s-%(index)s" value="o">Other / not sure</input></br>
        </td>
      </tr>
"""


IMG = u"""<img src="http://stats.ioinformatics.org/%s" />"""


if __name__ == "__main__":
    main()
