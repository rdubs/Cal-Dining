//
//  ViewController.swift
//  Cal-Dining
//
//  Created by Ranit Dubey on 8/4/15.
//  Copyright (c) 2015 Ranit Dubey. All rights reserved.
//

import UIKit
import Parse

class ViewController: UIViewController {
//    var entreesByDiningHall =  [String: [String: [PFObject]]]()
    var entreesByDiningHall = ["crossroads" : [String: [PFObject]](),
                                            "cafe3": [String: [PFObject]](),
                                            "foothill": [String: [PFObject]](),
                                            "ckc": [String: [PFObject]]()
    ]
    
    var halls =  ["crossroads",
                "cafe3",
                "foothill",
                "ckc"
    ]
    
    var meals =  ["Breakfast",
        "Lunch",
        "Dinner",
    ]
    
    var entrees: [PFObject] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        var query = PFQuery(className: "Entree")
        query.findObjectsInBackgroundWithBlock {
            (results: [AnyObject]?, error: NSError?) -> Void in
            if error == nil {
                self.entrees = results as! [PFObject]
                self.sortEntrees()
            }
        }
    }
    
    func sortEntrees() {
        for entree in self.entrees {
            var meal = entree["meal_type"] as! String
            var hall = entree["dining_hall"] as! String
            if let var mealArray = self.entreesByDiningHall[hall]![meal] {
                self.entreesByDiningHall[hall]![meal]!.append(entree)
            } else {
                self.entreesByDiningHall[hall]![meal] = []
            }
        }
    }
        
//        for meal_index in 0...2 {
//            var meal = self.meals[meal_index]
//            for index in 0...3 {
//                var hall = self.halls[index]
//                var predicate = NSPredicate(format: "dining_hall = '\(hall)' AND meal_type = 'Breakfast'")
//                var query = PFQuery(className: "Entree", predicate: predicate)
//                query.findObjectsInBackgroundWithBlock {
//                    (results: [AnyObject]?, error: NSError?) -> Void in
//                    if error == nil {
//                        self.entreesByDiningHall[hall]![meal] = results as! [PFObject]
//                        println(self.entreesByDiningHall)
//                    }
//                }
//            }
//        }
}
    


