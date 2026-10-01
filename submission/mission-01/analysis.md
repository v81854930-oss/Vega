Mission 01
At t=418s the GPS status changed to DEGRADED and the satellite count dropped from 10 to 5. It came back at t=421s, then dropped again at t=426s before fully recovering at t=429s.
While 1 time can be expected as a simple error 2 times is concerning
I think the balloon was rotating at that point and the antenna briefly lost line of sight to some satellites I need rool and pitch values at t=418s.
Some RF interference caused it to loose satellite data
I could not get YAMCS and Open MCT set up locally in reasonable time so I got a basic Screenshot page instead that shows the telemetry values and a text-based chart. The task says to document this if it happens.
I tried writing analyze_telemetry.py to read through the CSV and print a summary of all the channels and flag any sudden changes
On real hardware the dashboard would need to show live data also the text charts are pretty ugly, proper plots would be better.
