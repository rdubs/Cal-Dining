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
    var entreesByDiningHall =  [String: [String: [PFObject]]]()
    var halls =  ["crossroads",
                "cafe3",
                "foothill",
                "ckc"
    ]
    
    var meals =  ["Breakfast",
        "Lunch",
        "Dinner",
    ]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        for meal_index in 0...2 {
            var meal = self.meals[meal_index]
            for index in 0...3 {
                var hall = self.halls[index]
                var predicate = NSPredicate(format: "dining_hall = '\(hall)' AND meal_type = 'Breakfast'")
                var query = PFQuery(className: "Entree", predicate: predicate)
                query.findObjectsInBackgroundWithBlock {
                    (results: [AnyObject]?, error: NSError?) -> Void in
                    if error == nil {
                        self.entreesByDiningHall[hall]![meal] = results as! [PFObject]
                        print(results)
                        print("test")
                    }
                }
            }
        }
    }
        
    
    func test() {
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

