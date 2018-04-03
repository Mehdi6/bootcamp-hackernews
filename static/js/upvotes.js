$(document).ready(function() {
        var root_url = 'https://localhost:8000/services/'
        // Upvoting a topic via ajax requests
        $(".upvote_topic").click(function() {
            var parent = $(this)
            var topic_id = parent.attr("id")
            topic_id = topic_id.split("_")
            topic_id = topic_id[1]

            console.log(topic_id)

            $.ajax({
                url: root_url + 'topic/upvote/'+topic_id,
                type: 'get',
                success: function(data) {
                    if(data == 's'){
                        console.log("Topic upvoted successfuly!")
                        // Edit the number of points by increasing them +1
                        var score_markup_tag = "#score_"+topic_id
                        var score_markup = $(score_markup_tag)
                        console.log(score_markup)
                        var score = parseInt(score_markup.attr('upvotes'))
                        score += 1
                        score_markup.text(score + " points")
                        score_markup.attr('upvotes', score)
                        parent.remove()
                    }
                    else{
                        // TODO: Report error
                        console.log("Error during the upvote process.")
                    }
                },
                failure: function(data) {
                    alert('Got an error dude');
                }
            });
            }
        )
        // Upvoting a comment via ajax requests
        $(".upvote_comment").click(function() {
            var parent = $(this)
            var comment_id = parent.attr("id")
            comment_id = comment_id.split("_")
            comment_id = comment_id[1]
            var child = parent.find("span")

            $.ajax({
                url: root_url + 'comment/upvote/'+comment_id,
                type: 'get',
                success: function(data) {
                    if(data =='s'){
                        console.log("Comment upvoted successfuly!")
                        // Edit the number of points by increasing them +1

                        score = parseInt(child.attr('upvotes'))
                        score += 1
                        child.text("("+score+")")
                        removeUpvoteButton(parent)
                    }
                    else{
                        // TODO: Report error
                        console.log("Error during the upvote process!")
                    }
                },
                failure: function(data) {
                    // TODO: Report error
                    //alert('Got an error dude');
                }
            });

            }
        )

        function removeUpvoteButton(parent){
            button = parent.find("button")
            button.remove()
        }
    })