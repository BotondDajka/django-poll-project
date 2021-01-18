function homePage(){
    clearPage(function(){
        $("#title").html("Poll | Home");

        let $createButton = $(document.createElement("i"));
        $createButton.hide();
        $createButton.addClass("fas fa-plus create-button");
        $("#container").append($createButton);

        $createButton.click(function(){
            createPage();
        })


        $.get("http://localhost:8000/", function( data ) {
            $.each( data, function(key, val) {
                
                let $postit = $(document.createElement("div"));
                $postit.addClass("postit");
                $("#container").append($postit);

                let $title = $(document.createElement("p"));
                $title.addClass("postit-title");
                $title.append(val.question);
                $postit.append($title);

                let $options = $(document.createElement("ul"));
                $options.addClass("postit-text");

                let $option1 = $(document.createElement("li"));
                $option1.append(val.option_one);
                $options.append($option1);

                let $option2 = $(document.createElement("li"));
                $option2.append(val.option_two);
                $options.append($option2);

                let $option3 = $(document.createElement("li"));
                $option3.append(val.option_three);
                $options.append($option3);
                
                $postit.append($options);

                $postit.click(function(){
                    votePage(val.id);
                    document.documentElement.scrollTop = 0;
                    document.body.scrollTop = 0;
                })
            });
 

            $(".postit").each(function() {
                let num = (Math.floor((Math.random() * 10) + 1)-5);
                $(this).css('transform','rotate('+num+'deg)');
            });

            if (data.length == 0){
                let $empty = $(document.createElement("h1"));
                $empty.append("No available polls");
                $empty.addClass("no-polls-title");
                $("#container").append($empty);
            }

            
            $("#container").slideDown(800, function(){
                $createButton.fadeIn(300);
            }); 
        });
    });
}


function votePage(index){
    clearPage(function(){
        $("#title").html("Poll | Vote");
        $.get("http://localhost:8000/vote/"+index+"/", function(data) {
            let $postit = $(document.createElement("div"));
            $postit.addClass("postit-vote");
            $("#container").append($postit);

            let $title = $(document.createElement("p"));
            $title.addClass("postit-title");
            $title.append(data.question);
            $postit.append($title);


            let $options = $(document.createElement("ul"));
            $options.id = "options";
            $options.addClass("postit-tickbox");

            let option1 = document.createElement("input");
            option1.classList.add("pointer")
            option1.type = "radio";
            option1.id = "option1";
            option1.name = "options";
            option1.value = 1;
            $options.append(option1);

            let option1Label = document.createElement("label");
            option1Label.classList.add("pointer")
            option1Label.htmlFor = "option1";
            option1Label.innerHTML = "	&nbsp;	&nbsp;"+data.option_one;
            $options.append(option1Label);
            $options.append("<br>");

            let option2 = document.createElement("input");
            option2.classList.add("pointer")
            option2.type = "radio";
            option2.id = "option2";
            option2.name = "options";
            option2.value = 2;
            $options.append(option2);

            let option2Label = document.createElement("label");
            option2Label.classList.add("pointer")
            option2Label.htmlFor = "option2";
            option2Label.innerHTML = "	&nbsp;	&nbsp;"+data.option_two;
            $options.append(option2Label);
            $options.append("<br>");

            let option3 = document.createElement("input");
            option3.classList.add("pointer")
            option3.type = "radio";
            option3.id = "option3";
            option3.name = "options";
            option3.value = 3;
            $options.append(option3);

            let option3Label = document.createElement("label");
            option3Label.classList.add("pointer")
            option3Label.htmlFor = "option3";
            option3Label.innerHTML = "	&nbsp;	&nbsp;"+data.option_three;
            $options.append(option3Label);
            

            $postit.append($options);


            let $submit = $(document.createElement("div"));
            let $submitText =  $(document.createElement("p"));

            $submit.addClass("submit-button");
            $submitText.addClass("submit-text");
            $submitText.append("Submit");
            $submit.append($submitText);
            $postit.append($submit);

            let num = (Math.floor((Math.random() * 10) + 1)-5);
            $($submit).css('transform','rotate('+num+'deg)');

            $submit.click(function(){   
                let selectedOption = $('input[name=options]:checked', '.postit-tickbox').val();

                if (selectedOption == undefined){
                    alert("Option must selected!")
                }
                else{
                    $.ajax({
                        type: "PUT",
                        url: "http://localhost:8000/vote/"+index+"/",
                        contentType: "application/json",
                        data: JSON.stringify({option: selectedOption}),
                        success: function(){
                            resultsPage(index);
                        },
                    });
                }
            })

            
            let $results = $(document.createElement("div"));
            let $resultsText =  $(document.createElement("p"));

            $resultsText.addClass("result-text");
            $resultsText.append("Results");
            $results.append($resultsText);
            $postit.append($results);
            $results.addClass("result-button");

            num = (Math.floor((Math.random() * 10) + 1)-5);
            $($results).css('transform','rotate('+num+'deg)');

            $results.click(function(){   
                resultsPage(index)
            })
            
            $("#container").slideDown(800, function(){
                $(".body").height(($(".container").height()+300)+"px");
                generateHomeButton(function(button){
                    button.fadeIn(300);
                });
            }); 
        })
    })
}

function resultsPage(index){    
    clearPage(function(){
        $("#title").html("Poll | Result");
        $.get("http://localhost:8000/vote/"+index+"/", function( data ) {
            let $postit = $(document.createElement("div"));
            $postit.addClass("postit-vote");
            $("#container").append($postit);

            let $title = $(document.createElement("p"));
            $title.addClass("postit-title");
            $title.append(data.question);
            $postit.append($title);


            let $options = $(document.createElement("ul"));
            $options.id = "options";
            $options.addClass("postit-tickbox");

            let $option1 = $(document.createElement("li"));
            $option1.append(data.option_one);
            $options.append($option1);

            let $result1Cont = $(document.createElement("div"));
            $result1Cont.addClass("result-cont");
            let $result1Bar = $(document.createElement("div"));
            $result1Bar.addClass("result-bar");
            let $result1Per = $(document.createElement("p"));
            $result1Per.addClass("result-perc");

            $result1Bar.append($result1Per);
            $result1Cont.append($result1Bar);

            $options.append($result1Cont);


            let $option2 = $(document.createElement("li"));
            $option2.append(data.option_two);
            $options.append($option2);

            
            let $result2Cont = $(document.createElement("div"));
            $result2Cont.addClass("result-cont");
            let $result2Bar = $(document.createElement("div"));
            $result2Bar.addClass("result-bar");
            let $result2Per = $(document.createElement("p"));
            $result2Per.addClass("result-perc");

            $result2Bar.append($result2Per);
            $result2Cont.append($result2Bar);

            $options.append($result2Cont);


            let $option3 = $(document.createElement("li"));
            $option3.append(data.option_three);
            $options.append($option3);
                
            let $result3Cont = $(document.createElement("div"));
            $result3Cont.addClass("result-cont");
            let $result3Bar = $(document.createElement("div"));
            $result3Bar.addClass("result-bar");
            let $result3Per = $(document.createElement("p"));
            $result3Per.addClass("result-perc");

            $result3Bar.append($result3Per);
            $result3Cont.append($result3Bar);

            $options.append($result3Cont);


            $postit.append($options);


            let $vote = $(document.createElement("div"));
            let $voteText =  $(document.createElement("p"));

            $voteText.addClass("result-text");
            $voteText.append("Vote");
            $vote.append($voteText);
            $postit.append($vote);
            $vote.addClass("result-button");

            num = (Math.floor((Math.random() * 10) + 1)-5);
            $($vote).css('transform','rotate('+num+'deg)');

            $vote.click(function(){  
                votePage(index)    
            })

            $("#container").slideDown(800, function(){
                $(".body").height(($(".container").height()+300)+"px");
                let option1Per;
                let option2Per;
                let option3Per;

                let option1Count = data.option_one_count;
                let option2Count = data.option_two_count;
                let option3Count = data.option_three_count;

                let totalVotes = option1Count  + option2Count + option3Count;

                if (totalVotes > 0){
                    option1Per = Math.round(((option1Count / totalVotes) * 1000)) / 10;
                    option2Per = Math.round(((option2Count / totalVotes) * 1000)) / 10;
                    option3Per = Math.round(((option3Count / totalVotes) * 1000)) / 10;
                }
                else{
                    option1Per = 0;
                    option2Per = 0;
                    option3Per = 0;
                }

                $result1Bar.width(option1Per+"%");
                $result1Per.append(`${option1Per}% (${option1Count})`);

                $result2Bar.width(option2Per+"%");
                $result2Per.append(`${option2Per}% (${option2Count})`);

                $result3Bar.width(option3Per+"%");
                $result3Per.append(`${option3Per}% (${option3Count})`);

                generateHomeButton(function(button){
                    button.fadeIn(300)
                });
            });  
        });
    });    
}

function createPage(){ 
    $("#container").hide();
    $("#container").empty();


    let $postit = $(document.createElement("div"));
    $postit.addClass("postit-vote");
    $("#container").append($postit);

    let $postitTitle =  $(document.createElement("p"));
    $postitTitle.addClass("postit-title");

    let $questionInput = $(document.createElement("textarea"));

    $questionInput.attr("maxlength", "60");
    $questionInput.attr("placeholder", "Question...");
    $questionInput.addClass("input-field-question");

    $postitTitle.append($questionInput);
    $postit.append($postitTitle);


    let $options = $(document.createElement("ul"));
    $options.addClass("postit-tickbox");

    let $option1Input = $(document.createElement("input"));
    $option1Input.attr("maxlength", "30");
    $option1Input.attr("placeholder", "Option 1");
    $option1Input.addClass("input-field");

    $options.append($option1Input);

    let $option2Input = $(document.createElement("input"));
    $option2Input.attr("maxlength", "30");
    $option2Input.attr("placeholder", "Option 2");
    $option2Input.addClass("input-field");

    $options.append($option2Input);

    let $option3Input = $(document.createElement("input"));
    $option3Input.attr("maxlength", "30");
    $option3Input.attr("placeholder", "Option 3");
    $option3Input.addClass("input-field");

    $options.append($option3Input);


    $postit.append($options);

    let $submit = $(document.createElement("div"));
    let $submitText =  $(document.createElement("p"));

    $submit.addClass("submit-button");
    $submitText.addClass("submit-text");
    $submitText.append("Submit");
    $submit.append($submitText);
    $postit.append($submit);

    let num = (Math.floor((Math.random() * 10) + 1)-5);
    $($submit).css('transform','rotate('+num+'deg)');

    $submit.click(function(){
        if ($questionInput.val() && $option1Input.val() && $option2Input.val() && $option3Input.val()){
            $.post("http://localhost:8000/create/",
            {
                question: $questionInput.val(),
                option_one: $option1Input.val(),
                option_two: $option2Input.val(),
                option_three:$option3Input.val()
            },
            function(data){
                $("#container").slideUp(400,function(){
                    homePage();
                })
            });
        }
        else{
            alert("All fields must be filled before submiting!");
        }
    })

    $("#container").slideDown(800, function(){
        generateHomeButton(function(button){
            button.fadeIn(300);
        });
    }); 
}


async function generateHomeButton(button){
    let $homeButton = $(document.createElement("i"));
    $homeButton.hide();
    $homeButton.addClass("fas fa-home home-button");

    $homeButton.click(function(){
        $("#container").slideUp(400,function(){
            homePage();
        });
    })
    $("#container").append($homeButton);

    button($homeButton)
}

async function clearPage(done){
    $("#container").slideUp(400,function(){
        $("#container").empty();
        done()
    });
}


$("#container").hide();
homePage();