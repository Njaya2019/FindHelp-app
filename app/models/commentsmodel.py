"""
This is a comment model, it creates, edits and deletes comments
"""

from .dataBase import db
import os
from os import remove


class comments():

    @staticmethod
    def postAcomment(con_cur, comment, answerid, userid):
        """ A static method to add an comment on a an answer """
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findUser_sql = "SELECT * FROM users WHERE userid=%s"
            cur.execute(findUser_sql, (userid,))
            # if there are no rows fetchall returns an empty list.
            userExists = cur.fetchone()
            if userExists:
                findAnswer_sql = "SELECT * FROM answers WHERE answerid=%s"
                cur.execute(findAnswer_sql, (answerid,))
                answerExists = cur.fetchone()
                if answerExists:
                    postComment_sql = "INSERT INTO comments(comment,answerid,userid,timecommented) VALUES(%s,%s,%s,CURRENT_TIMESTAMP) RETURNING comment, answerid, userid, timecommented"
                    commentData = (comment, answerid, userid,)
                    cur.execute(postComment_sql, commentData)
                    con.commit()
                    postedComment = cur.fetchone()
                    return postedComment
                else:
                    # 'The answer you commenting on doesn\'t exist'
                    return 'answer not found'
            else:
                # 'The user commenting doesn't exist'
                return 'user not found'
        except Exception as err:
            print(err)

    @staticmethod
    def editAcomment(con_cur, comment, commentid, userid):
        """ A static method to edit a comment """
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findComment_sql = "SELECT * FROM comments WHERE commentid=%s"
            cur.execute(findComment_sql, (commentid,))
            # if there are no rows fetchall returns an empty list.
            commentExists = cur.fetchone()
            if commentExists:
                # Checks if the user exists
                findUser_sql = "SELECT * FROM users WHERE userid=%s"
                cur.execute(findUser_sql, (userid,))
                userExists = cur.fetchone()
                if userExists:
                    if commentExists['userid'] != userid:
                        # 'You can not edit other users comments'
                        return 'not owner'
                    else:
                        editComment_sql = "UPDATE comments SET comment=%s WHERE commentid=%s"
                        editCommentData = (comment, commentid,)
                        cur.execute(editComment_sql, editCommentData)
                        con.commit()
                        get_comment_sql ="SELECT users.fullname, users.userid, comments.commentid, comments.comment FROM users INNER JOIN comments ON users.userid = comments.userid WHERE comments.commentid=%s and users.userid=%s"
                        getCommentData = (commentid, userid,)
                        cur.execute(get_comment_sql, getCommentData)
                        commentFetched = cur.fetchone()
                        return commentFetched
                else:
                    # 'The user editting the comment doesn\'t exist'
                    return 'user not found'
            else:
                # 'The comment doesn't exist'
                return 'comment not found'
        except Exception as err:
            print(err)


    @staticmethod
    def deleteAcomment(con_cur, commentid, userid):
        """ A static method to delete a comment """
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findComment_sql = "SELECT * FROM comments WHERE commentid=%s"
            cur.execute(findComment_sql, (commentid,))
            # if there are no rows fetchall returns an empty list.
            commentExists = cur.fetchone()
            if commentExists:
                # Checks if the user exists
                findUser_sql = "SELECT * FROM users WHERE userid=%s"
                cur.execute(findUser_sql, (userid,))
                userExists = cur.fetchone()
                if userExists:
                    if commentExists['userid'] != userid:
                        # 'You can not delete other users comments'
                        return 'not owner'
                    else:
                        deleteComment_sql = "DELETE FROM comments WHERE commentid=%s RETURNING commentid"
                        deleteCommentData = (commentid,)
                        cur.execute(deleteComment_sql, deleteCommentData)
                        con.commit()
                        deletedComment = cur.fetchone()
                        return deletedComment
                else:
                    # 'The user deleting the comment doesn\'t exist'
                    return 'user not found'
            else:
                # 'The comment you want to delete doesn't exist'
                return 'comment not found'
        except Exception as err:
            print(err)
