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
    
    var diningHalls : [PFObject] = [PFObject]()
    var entrees : [PFObject] = [PFObject]()

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        let predicate = NSPredicate(format: "dining_hall = 'ckc' AND meal_type = 'Dinner'")
        var query = PFQuery(className: "Entree", predicate: predicate)
        query.findObjectsInBackgroundWithBlock {
            (results: [AnyObject]?, error: NSError?) -> Void in
            if error == nil {
                // results contains players with lots of wins or only a few wins.
                print(results)
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

