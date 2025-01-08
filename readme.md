# Daily Script

## Context: 

I've redacted any sensitive data in order to use this code as a platform to showcase my skill as a novice programmer. At Greetabl, our factory in Memphis, TN shut down with less than 3 months notice. We were already in panic as our dev team was unavailable to renew their contract and our employees had all transitioned to new jobs in response to a recent aquisition. I started desparatly writing this code sometime in June, only being comfortable of touching GitHub with my first commit on July 17, 2023.

# What this code does:

main.py is the script that acts as a hub where you can access all the functions written for this code.

1.) Run daily query
2.) Update statuses before a given date
3.) Process individual orders
4.) Process individual builds
5.) Group PDFs and overlay regmarks
6.) Exit

1. This is what the code is primarily used for. It gathers data from greetabl.com and outputs a PDF and CSV for order fulfillment.
2. This was originally a debugging tool, albeit not quiet polished. It's primary goal was to reset dates in order to get them back into the fulfillment process.
3+4. These allowed modifications to the shipment status of orders and builds, pushing them back into the fulfillment process.
5. For PDFs with more customized approaches, this would output a PDF with registration marks for fulfillment. 
6. Terminates process

The other scripts are just dependencies for executing these main functions. 

# Credit 

I worked on this with one other colaborator who joined our team after most of this code's development was complete. They tidied up the code and added QoL modifications. I take credit for most of the functional aspects. I'd also attribute a lot of the coding clean up to ChatGPT 3.5, I specify the version because with more modern versions ChatGPT is much more sophisticated at providing functional and legible code, meaning I had a more involved role in the creation of this code. For example, even modern versions of ChatGPT totally fail any ability to format and adjust elements on a PDF.
