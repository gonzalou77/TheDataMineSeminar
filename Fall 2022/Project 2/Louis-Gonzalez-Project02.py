
#Question 1

"""A one line summary of the module or program, terminated by a period.

Serialization is a process by which a data object is converted into a format that allows the transmission of data which then reconstruct the object by deserialization when the object is needed. Examples of when serialization is used include sending an object to a remote application by a web service, pass an object from one domain to another and more. Some serialization formats commonly used are JSON or XML formats.

Deserialization is the reverse process of serialization by which data which was previously serialized or structured into data is reconstructed to its original object state. Certain functions in python are capable of this such as pickle. This is also commonly used in cyber attacks.


JSON for example returns data as human readable strings while pickle (python library) returns a byte array. Each one has its uses, for example JSON format is excellent for structures data bases, but can take quite a bit of hardrive space. 

As for pickle, the data is much more compact and faster to process since the data is in a computer readable format (or non-human readable if that makes sense) which is less computationally expensive and requires less harddrive space but may be difficult to manage since the data must be converted to a human readable format.

Two broad categories that serialized data can be categorized would be as human readable or non-human readable. For non-human readable or computer readable , this refers to having a format which only the computer may understand which could me a memory address or hexadecimal object etc.

Source: 
https://machinelearningmastery.com/a-gentle-introduction-to-serialization-for-python/
https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/serialization/
https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html

"""