John Moore
Inventory and Purchase Order System Program

1.) What part of the project was hardest?

    The hardest part of this project was probably the planning and execution of the project, outside of the tedious small bugs that came through due to syntax mistakes. Trying to plan ahead and think about the best way to build this up piece by piece while keeping separation of concerns was more troublesome than I initially anticipated, especially on the more complex files like the inventory_manager file. Building functions and not being able to test them in the way they are practically used from file to file proved difficult. I realized that having the JSON file ready before the read and save functions was shortsighted and made me realize there was a smarter way to build this up. I learned that building in a logical order where each file depends on the ones before it would have saved time and reduced confusion early on.


2.) What bug took the longest to solve?

    The most notable bug was probably the clearance items report. I ran into an issue comparing the clearance date to today's date. It was more complicated than I realized due to how JSON stores dates as strings. This created an interesting situation where I had to think through the process of taking a string and converting it into a date data type that could be used in a comparison. I found that Python's datetime module provides a date class
    with a today() method that returns today's date. The fix was converting the stored clearance date string into a matching date object using date.fromisoformat() so the two could be compared directly.

3.) How did you organize your code across multiple files?

	I tried to use the separations of concerns principle and split it into sections that solved different problems that an inventory management program introduces. Each one of the files then was designed address the different types of objects or processes that happen in an inventory management system or something you would see in a formal ERP system. The models.py file was built first given the objects and classes are the foundation to the rest of the files and functions that were created. File_manager.py was made so that all the products, vendors, and transactions were saved between sessions and persisted, giving the program actual value when being used. Inventory_manager.py is like the brain of the program and contains all the logic that handles the data and transforms it based on the different features or functions that were required to handle the needs of an inventory management system. reports.py was kept separate so all reporting functions had their own dedicated space and did not mix with the business logic in inventory_manager.py. main.py acts purely as the user interface, connecting the user to the right function without doing any work itself, similar to a telephone operator connecting a call.

4.) How does your save/load system work?

    When saving, the program converts all product, vendor, and purchase order objects
    into dictionaries using their to_dict() methods, which are very similar but suited to the data structure of each of those classes. These dictionaries are then combined into one dictionary for storage and written to the store_data.json file using json.dump(). When loading, the program reads store_data.json using json.load(), which returns the combined dictionary and each section is converted back into objects using the from_dict() method. Similar to the to_dict methods, these are designed specific to the class’s structure. The way the objects are packed is essentially the opposite of how they are unpacked.


5.) What would you improve if you had another week?

    I had a couple ideas that I thought about while building this out that would be cool to implement if I had more time. First I thought about having something that would automatically reduce products prices based on their clearance date. This would require things to be ordered and separated in lots given that products could have different clearance dates depending on when they were received. There would also have to be some additional logic that would scan and adjust inventory on a fixed time interval.

    I also thought about adding something that would add some sales metrics to the system. These reports could give you the highest selling products or ones that seemed to be sitting in inventory too long and could have their restock thresholds adjusted so sitting inventory is reduced, creating capacity for other products that have higher value.


