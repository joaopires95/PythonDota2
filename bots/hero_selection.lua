function Think()

	if ( GetTeam() == TEAM_RADIANT )
	then
		print( "selecting radiant" );
		SelectHero( 2, "npc_dota_hero_templar_assassin" );
		SelectHero( 3, "npc_dota_hero_sven" );
		SelectHero( 4, "npc_dota_hero_sven" );
		SelectHero( 5, "npc_dota_hero_sven" );
		SelectHero( 6, "npc_dota_hero_sven" );
		
	elseif ( GetTeam() == TEAM_DIRE )
	then
		print( "selecting dire" );
		SelectHero( 7, "npc_dota_hero_ursa" );
		SelectHero( 8, "npc_dota_hero_sven" );
		SelectHero( 9, "npc_dota_hero_sven" );
		SelectHero( 10, "npc_dota_hero_sven" );
		SelectHero( 11, "npc_dota_hero_sven" );
	end
	
end
