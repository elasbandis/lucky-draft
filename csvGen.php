<?php

function extractNumbers($file) {
    echo "Processing file: $file\n";
    
    // Read the file content as text instead of parsing as HTML
    $content = file_get_contents($file);
    
    if ($content === false) {
        echo "Could not read file: $file\n";
        return [];
    }
    
    $results = [];
    
    // Look for sections with class="balls" followed by resultBall elements
    // The pattern matches from the formatted HTML spans to &lt;/ul&gt;
    preg_match_all('/<span class="html-attribute-value">balls<\/span>"&gt;<\/span>.*?&lt;\/ul&gt;/s', $content, $ballSections);
    
    echo "Found " . count($ballSections[0]) . " ball sections in $file\n";
    
    foreach ($ballSections[0] as $ballSection) {
        // Extract main balls (resultBall ball small)
        preg_match_all('/<span class="html-attribute-value">resultBall ball small<\/span>"&gt;<\/span>(\d+)<span class="html-tag">&lt;\/li&gt;<\/span>/', $ballSection, $mainBallMatches);
        
        // Extract lucky stars (resultBall lucky-star small)
        preg_match_all('/<span class="html-attribute-value">resultBall lucky-star small<\/span>"&gt;<\/span>(\d+)<span class="html-tag">&lt;\/li&gt;<\/span>/', $ballSection, $luckyStarMatches);
        
        if (!empty($mainBallMatches[1])) {
            $mainBalls = $mainBallMatches[1];
            $luckyStars = isset($luckyStarMatches[1]) ? $luckyStarMatches[1] : [];
            
            echo "Found main balls: " . implode(', ', $mainBalls) . "\n";
            echo "Found lucky stars: " . implode(', ', $luckyStars) . "\n";
            
            if (count($mainBalls) >= 5) {  // Ensure we have at least 5 main balls
                $results[] = [
                    'date' => basename($file, '.html'),
                    'main_balls' => array_slice($mainBalls, 0, 5),  // Take exactly 5 main balls
                    'lucky_stars' => array_slice($luckyStars, 0, 2)  // Take exactly 2 lucky stars
                ];
            }
        }
    }

    // Reorder resuults 
    $results = array_reverse($results);

    
    echo "Extracted " . count($results) . " lottery draws from $file\n";
    return $results;
}

// Open CSV file for writing
$csvFile = fopen('lottery_results.csv', 'w');

// Write CSV header
fputcsv($csvFile, ['Date', 'Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5', 'Lucky Star 1', 'Lucky Star 2']);

// Get all HTML files from results directory
$files = glob(__DIR__ . '/results/*.{html,htm}', GLOB_BRACE);

foreach ($files as $file) {
    $results = extractNumbers($file);
    
    foreach ($results as $result) {
        $row = array_merge(
            [$result['date']],
            array_pad($result['main_balls'], 5, ''),  // Ensure we have 5 main balls
            array_pad($result['lucky_stars'], 2, '')   // Ensure we have 2 lucky stars
        );
        fputcsv($csvFile, $row);
    }
}

fclose($csvFile);

echo "CSV file has been generated successfully!\n";