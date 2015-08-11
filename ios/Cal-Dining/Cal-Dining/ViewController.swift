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
    
    var jsonDiningData : [PFObject] = [PFObject]()

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        var query = PFQuery(className:"DiningHall")
        query.findObjectsInBackgroundWithBlock {
            (objects: [AnyObject]?, error: NSError?) -> Void in
            
            if error == nil {
                // The find succeeded.
                println("Successfully retrieved \(objects!.count) scores.")
                // Do something with the found objects
                if let objects = objects as? [PFObject] {
                    self.jsonDiningData = objects
                    print(objects)
                }
            } else {
                // Log details of the failure
                println("Error: \(error!) \(error!.userInfo!)")
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

