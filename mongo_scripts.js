/**
 * Created by nitinp on 7/10/17.
 */

// Fetch user, review count

db.yelp.aggregate([{$group: {_id: "$user_id", count: {$sum: 1}}}, {$match: {count: {$gt: 100}}}]);